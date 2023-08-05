# MIT License

# Copyright (c) 2018 Bobby

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    from _inotify import ffi, lib
except ImportError as e:
    raise ImportError("{}\nMake sure you ran 'python3 inotify_build.py'."
                      .format(e, __name__))


import asyncio
import errno
import logging
import operator
import os
import selectors
import struct
import sys
import time
from collections import OrderedDict, defaultdict, deque
from functools import reduce, wraps
from glob import glob
from itertools import chain
from pathlib import Path

__all__ = ['watcher', 'run', 'add_watcher',
           'remove_watcher', 'remove_watchers', 'Event']


class Error(Exception):
    pass


class InitializationError(Error):

    def __init__(self, settings):
        self.settings = settings

    def __str__(self):
        return("Failed to initialize inotify with settings={!r} ({})"
               .format(self.settings, os.strerror(ffi.errno)))


class InvalidEventNamesError(Error):

    def __init__(self, invalid_event_names):
        self.names = list(invalid_event_names)

    def __str__(self):
        names = list("'{}'".format(name) for name in self.names)
        return ('{} not found in {module}.EVENTS or {module}.VEVENTS'
                .format(', '.join(names), module=__name__))


class WatcherNotFoundError(Error):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return ("There are no existing watchers on path={}".format(path))


class HandlerNotFoundError(Error):

    def __init__(self, event):
        self.event = event

    def __str__(self):
        return ("There are no existing handlers for event={}"
                .format(self.event))


# file descriptor for inotify
_inotify_fd = -1

# logger
logger = None


class Event:
    """An Event passed to a Watcher.
    """
    __slots__ = ('_wd', '_flags', '_vflags', '_cookie',
                 'filename', 'path', 'source', 'destination', 'vhandler')

    def __init__(self, wd, flags, cookie, filename, *,
                 path=None, source='', destination='',
                 vflags=0, vhandler=None):
        self._wd = wd
        self._flags = flags
        self._cookie = cookie
        self._vflags = vflags
        self.filename = filename
        self.path = path  # path of this object filled in by dispatch
        self.source = source  # set by moved_from/moved/relocated
        self.destination = destination  # set by moved_to/moved/relocated
        self.vhandler = vhandler  # set by create_virtual_event

    @property
    def wd(self):
        "Watch descriptor number."
        return self._wd

    @property
    def flags(self):
        "Flags indicating which events we handle."
        return self._flags

    @property
    def vflags(self):
        "Flags indicating which virtual events we handle."
        return self._vflags

    @property
    def cookie(self):
        "Cookie indicating related move events."
        return self._cookie

    def __repr__(self):
        name = type(self).__name__
        return ("{}(wd={!r}, flags={!r}, cookie={!r}, "
                " filename={!r}, vflags={!r})"
                .format(name, self.wd, self.flags, self.cookie,
                        self.filename, self.vflags))

    def __str__(self):
        name = type(self).__name__
        return ("{}(wd={!r}, flags={!r}, cookie={!r}, "
                " filename={!r}, path={!r}, vflags={!r})"
                .format(name, self.wd, self.flags, self.cookie,
                        self.filename, self.path, self.vflags))

    @property
    def _key(self):
        return (self.wd, self.flags, self.cookie, self.filename)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        if isinstance(other, Event):
            return self._key == other._key
        else:
            return NotImplemented

    def __lt__(self, other):
        return (self.wd, self.filename) < (other.wd, other.filename)

    def __le__(self, other):
        return (self.wd, self.filename) <= (other.wd, other.filename)

    def __gt__(self, other):
        return (self.wd, self.filename) > (other.wd, other.filename)

    def __ge__(self, other):
        return (self.wd, self.filename) >= (other.wd, other.filename)

    @property
    def is_virtual(self):
        "True if this event is virtual."
        return bool(self.vflags)

    @property
    def is_directory(self):
        "True if this event relates to a directory."
        return self.flags & lib.IN_ISDIR

    @property
    def is_file(self):
        "True if this event relates to a non-directory."
        return not self.is_directory

    @property
    def is_move_event(self):
        "True if this event is related to fileobjects moving or being renamed."
        return self.flags & lib.IN_MOVE

    """
        Computed properties for checking flags.
    """

    @property
    def all(self):
        "True if we watch all events."
        return self.flags & lib.IN_ALL_EVENTS

    @property
    def created(self):
        "Filesystem object was created."
        return self.flags & lib.IN_CREATE

    @property
    def opened(self):
        "Filesystem object was opened."
        return self.flags & lib.IN_OPEN

    @property
    def accessed(self):
        "Filesystem object was accessed."
        return self.flags & lib.IN_ACCESS

    @property
    def modified(self):
        "Filesystem object was modified."
        return self.flags & lib.IN_MODIFY

    @property
    def deleted(self):
        "Filesystem object was deleted."
        return self.flags & lib.IN_DELETE

    @property
    def disappeared(self):
        "The file object we are watching was deleted."
        return self.flags & lib.IN_DELETE_SELF

    @property
    def relocated(self):
        "The file object we are watching was moved."
        return self.flags & lib.IN_MOVE_SELF

    @property
    def changed(self):
        "Filesystem object attributes were changed."
        return self.flags & lib.IN_ATTRIB

    @property
    def closed(self):
        "Filesystem object was closed."
        return self.flags & lib.IN_CLOSE

    @property
    def written(self):
        "Filesystem object was closed after being opened for writing."
        return self.flags & lib.IN_CLOSE_WRITE

    @property
    def read(self):
        "Filesystem object was closed without being written."
        return self.flags & lib.IN_CLOSE_NOWRITE

    @property
    def moved_from(self):
        "Filesystem object was moved from directory."
        return self.flags & lib.IN_MOVED_FROM

    @property
    def moved_into(self):
        "Filesystem object was moved into directory."
        return self.flags & lib.IN_MOVED_TO

    @property
    def unmounted(self):
        "Filesystem object was unmounted."
        return self.flags & lib.IN_UNMOUNT

    @property
    def overflowed(self):
        """inotify queue has overflowed. Check /proc/sys/fs/inotify/ for
        settings."""
        return self.flags & lib.IN_Q_OVERFLOW

    @property
    def ignored(self):
        "Filesystem object has stopped being watched by inotify."
        return self.flags & lib.IN_IGNORED

    # Virtual events

    @property
    def added(self):
        "Handler will now be dispatched events."
        return self.vflags & VEVENTS['added']

    @property
    def removed(self):
        "Handler will no longer be dispatched events."
        return self.vflags & VEVENTS['removed']

    @property
    def moved(self):
        "Filesystem object was moved and we were watching both directories."
        return self.vflags & VEVENTS['moved']

    @property
    def renamed(self):
        "Filesystem object was renamed."
        return self.vflags & VEVENTS['renamed']


class Watcher:
    __slots__ = ('flags', 'options', 'handler',
                 'path', 'vflags', 'recursive')

    def __init__(self, flags, options, handler, path, vflags, recursive):
        self.flags = flags
        self.options = options
        self.handler = handler
        self.path = path
        self.vflags = vflags
        self.recursive = recursive

    def __repr__(self):
        name = type(self).__name__
        return ("{}(flags={!r}, options={!r}, handler={!r}, "
                " path={!r}, vflags={!r}, recursive={!r})"
                .format(name, self.flags, self.options, self.handler,
                        self.path, self.vflags, self.recursive))

    # A watcher with the same __qualname__ may be handling different events in
    # different instantiations but when dispatching virtual events two watchers
    # are the same if the __qualname__ matches.
    def __eq__(self, other):
        return self.handler.__qualname__ == other.handler.__qualname__

    def __hash__(self):
        return hash(self.handler.__qualname__)


# dictionary {wd: [Watcher, ...]}
_watchers = defaultdict(list)

EVENTS = {
    'all': lib.IN_ALL_EVENTS,  # all events inotify man page for details
    'created': lib.IN_CREATE,  # file/directory was created
    'opened': lib.IN_OPEN,  # file/directory was opened
    'accessed': lib.IN_ACCESS,  # file/directory was accessed
    'modified': lib.IN_MODIFY,  # file/directory was modified
    'deleted': lib.IN_DELETE,  # file/directory was deleted
    'changed': lib.IN_ATTRIB,  # metadata was changed
    'closed': lib.IN_CLOSE,  # file/directory was closed
    'written': lib.IN_CLOSE_WRITE,  # file opened for writing was closed
    'read': lib.IN_CLOSE_NOWRITE,  # file/dir not opened for writing was closed
    'moved': lib.IN_MOVE,  # either a moved_from or moved_into event
    'moved_from': lib.IN_MOVED_FROM,  # file moved from this directory
    'moved_into': lib.IN_MOVED_TO,  # file moved to this directory
    'disappeared': lib.IN_DELETE_SELF,  # watched file/directory was deleted
    'relocated': lib.IN_MOVE_SELF,  # watched file/directory was moved
    'unmounted': lib.IN_UNMOUNT,  # filesystem containing object was unmounted
    'ignored': lib.IN_IGNORED,  # watch was removed
}

# Virtual event flags
# NOTE: Separate virtual events to avoid conflicting with future
# The difference between a inotify event and a virtual event should be
# transparent to the user.

VEVENTS = {
    'added': 0x00000001,
    'removed': 0x00000002,
    'moved': 0x00000004,
    'renamed': 0x00000008
}

VEVENTS['all_virtual'] = reduce(operator.ior, VEVENTS.values(), 0)

_eventq = asyncio.Queue()


def _read_inotify_settings():
    """
        Read inotify configuration information.
    """
    global logger

    inotify_dir = '/proc/sys/fs/inotify/'
    settings = ['max_queued_events', 'max_user_instances', 'max_user_watches']
    props = {}
    for setting in settings:
        try:
            with open(os.path.join(inotify_dir, setting),
                      encoding='utf-8') as s:
                props[setting] = int(s.read().strip())
        except FileNotFoundError as e:
            logger.warning(e)
        except IOError as e:
            logger.warning(e, exc_info=True)
            continue

    return props


def _make_options(follow_symlinks, exclude_unlink,
                  one_shot, only_directories):
    """Make a flag from arguments.
    """
    options = 0

    if not follow_symlinks:
        options |= lib.IN_DONT_FOLLOW

    if exclude_unlink:
        options |= lib.IN_EXCL_UNLINK

    if one_shot:
        options |= lib.IN_ONESHOT

    if only_directories:
        options |= lib.IN_ONLYDIR

    return options


def _expand_path(path):
    """Take a str and expand to list of paths.
    """
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    return glob(path)


def _validate_watcher(paths, events):
    try:
        paths = paths.split()
    except AttributeError:
        pass

    try:
        events = events.split()
    except AttributeError:
        pass

    # NOTE: invalid paths are ignored
    expanded_paths = []
    for path in paths:
        expanded_paths.extend(_expand_path(path))

    events = set(events)

    invalid = [e for e in events
               if e not in EVENTS and e not in VEVENTS]
    if invalid:
        raise InvalidEventNamesError(invalid)

    vevents = [e for e in events if e in VEVENTS]
    events = [e for e in events if e in EVENTS]

    return expanded_paths, events, vevents


def watcher(paths, events, *,
            follow_symlinks=True, exclude_unlink=False,
            one_shot=False, only_directories=False, recursive=False):
    """Adds this function as the handler for the given paths and responding to
    given events. path/events should be a space separated string or iterable of
    file and/or directory paths.
    """

    paths, events, vevents = _validate_watcher(paths, events)

    options = _make_options(follow_symlinks, exclude_unlink,
                            one_shot, only_directories)

    def decorator(fn):
        _add_watcher(paths, events, vevents, fn, options, recursive)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def _append_watcher(wd, watcher):
    global _watchers
    _create_virtual_event('added', watcher)
    _watchers[wd].append(watcher)


def _delete_watchers(wd):
    global _watchers
    for watcher in _watchers[wd]:
        _create_virtual_event('removed', watcher)
    try:
        del _watchers[wd]
    except KeyError:
        # This should never happen.
        raise WatcherNotFoundError('')


class EventStore(OrderedDict):

    def __init__(self, *args, max_len, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.max_len = max_len

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        super().__setitem__(key, value)
        if len(self) > self.max_len:
            self.popitem(last=False)

    def get(self, key):
        # NOTE: Currently cookies only apply to moved_from moved_into
        # So, we can remove the event here since it was handled.
        value = super().get(key, None)
        if value is not None:
            del self[key]
        return value


_move_events = EventStore(max_len=256)


def _add_move_event(event):
    """Place a move event in for later matching by cookie.
    """
    global _move_events

    first_event = _move_events.get(event.cookie)

    if first_event:
        src = event.source or first_event.source
        dst = event.destination or first_event.destination
        move_event = Event(-1, 0, 0, event.filename,
                           source=src, destination=dst)
        if first_event.wd == event.wd:
            for watcher in _watchers[event.wd]:
                _create_virtual_event('renamed', watcher, move_event)
        else:
            handlers = set(watcher
                           for watcher in
                           chain(_watchers[first_event.wd],
                                 _watchers[event.wd]))
            for watcher in handlers:
                _create_virtual_event('moved', watcher, move_event)
    else:
        _move_events[event.cookie] = event


def _create_virtual_event(vevents, watcher, event=None):
    """Create a virtual event for later handling by _handle_event.
    """
    try:
        vevents = vevents.split()
    except AttributeError:
        pass

    vevents = set(vevents)
    try:
        vmask = reduce(operator.ior, (VEVENTS[ve] for ve in vevents), 0)
    except KeyError:
        raise InvalidEventNamesError(ve for ve in vevents if ve not in VEVENTS)

    # virtual events apply to handlers and not paths and so Events have a
    # vhandler attribute that can be used to send an event to a particular
    # handler rather than a watcher. Doesn't feel quite right though.
    if vmask & watcher.vflags:
        path = Path(watcher.path)
        if event:
            # handle a custom event
            _dispatch_event(
                Event(event.wd, event.flags, event.cookie,
                      filename=event.filename,
                      path=path / event.filename, vflags=vmask,
                      source=event.source,
                      destination=event.destination,
                      vhandler=watcher.handler))
        else:
            # send basic virtual event with just vflags set
            _dispatch_event(
                Event(-1, 0, 0, path.name,
                      path=path, vflags=vmask,
                      vhandler=watcher.handler))


def add_watcher(paths, events, handler, *,
                follow_symlinks=True, exclude_unlink=False,
                one_shot=False, only_directories=False, recursive=False):
    """Add a new watcher or change an existing watcher.
    """

    paths, events, vevents = _validate_watcher(paths, events)

    options = _make_options(follow_symlinks, exclude_unlink,
                            one_shot, only_directories)

    _add_watcher(paths, events, vevents, handler, options, recursive)


def remove_watcher(handler):
    """Remove a given handler from watchers.
    """
    global _watchers
    # FIXME: for now just send directly; we would like cleaner solution
    _dispatch_event(
        Event(-1, 0, 0, '',
              path='', vflags=VEVENTS['removed'],
              vhandler=handler))
    _watchers.update({k: [w for w in lst if w.handler != handler]
                      for k, lst in _watchers.items()})


def remove_watchers(path):
    """Remove all watchers on given path.
    """
    global _watchers, logger

    path = Path(path).absolute()

    # linear search through all watchers for matching path
    for wd, watchers in _watchers.items():
        assert _watchers[wd], "all wd must have at least one watcher"
        assert all(watcher.path == _watchers[wd][0].path
                   for watcher in _watchers[wd]), "all watchers "
        "with the same wd must have the same path"

        watcher = watchers[0]
        if watcher.path.absolute() == path:
            break
    else:
        raise WatcherNotFoundError(path)

    ret = lib.inotify_rm_watch(_inotify_fd, wd)
    if ret == -1:
        # FIXME: should we raise exception here?
        logger.warning("Could not remove {!r} [{}]"
                       .format(path.as_posix(), os.strerror(ffi.errno)))
    else:
        # delete regardless of failure so we don't handle this wd
        _delete_watchers(wd)


def _add_watcher(paths, events, vevents, handler, options, recursive):
    """Add watcher using inotify_add_watch.
    """
    global _watchers, logger

    if _inotify_fd < 0:
        _initialize()

    paths = list(paths)

    for path in paths:
        mask = reduce(operator.ior, (EVENTS[e] for e in events), 0)
        vmask = reduce(operator.ior, (VEVENTS[ve] for ve in vevents), 0)

        wd = lib.inotify_add_watch(_inotify_fd, path.encode(),
                                   mask | options | lib.IN_MASK_ADD)

        # NOTE: while event is added inotify may have missed events related to
        # the object we are trying now to watch.
        # By handling 'added' virtual event they can perform workarounds for
        # possible missed events.
        # A handler can scan an added dir for missed files, for example.
        # Virtual events are handled in _append_watcher and _delete_watchers

        if wd < 0:
            # NOTE: Race conditions may cause a path to fail to be added in
            # certain conditions that do not seem easily resolvable. So, we log
            # a warning only here.
            logger.warning("Could not add {!r} [{}]"
                           .format(path, os.strerror(ffi.errno)))
        else:
            logger.debug("adding wd={} path={} handler={}"
                         .format(wd, path, handler))
            _append_watcher(wd, Watcher(mask, options,
                                        handler,
                                        Path(path),
                                        vmask,
                                        recursive))


def _copy_watcher(watcher, path):
    """Copy a watcher on a different path.
    """
    global _inotify_fd, _watchers

    # Before making the add_watch call a directory may be replaced with a
    # non-directory of the same name.
    watcher.options |= lib.IN_ONLYDIR

    logger.debug('copy watcher={} onto path={}'.format(watcher, path))

    wd = lib.inotify_add_watch(_inotify_fd, path.as_posix().encode(),
                               watcher.flags | watcher.options |
                               lib.IN_MASK_ADD)

    if wd < 0:
        # NOTE: info about race condition in _add_watcher applies here as well
        logger.warning("Could not copy onto path {!r} [{}]"
                       .format(path, os.strerror(ffi.errno)))
    else:
        _append_watcher(wd, Watcher(watcher.flags, watcher.options,
                                    watcher.handler,
                                    Path(path), watcher.vflags,
                                    watcher.recursive))


def _initialize():
    global _inotify_fd, settings, logger, _selector

    logger = logging.getLogger(__name__)

    settings = _read_inotify_settings()

    logger.debug('Initializing inotify.')
    _inotify_fd = lib.inotify_init1(lib.IN_NONBLOCK)

    if _inotify_fd < 0:
        raise InitializationError(settings)


def _make_reader(event_buffer_len=65536, delay=0.1):
    """Read a large amount of events into the given queue. event_buffer_len
    determines how much to attempt to read at once
    """
    logger.debug("Create reader buffer={} delay={}"
                 .format(event_buffer_len, delay))

    def _read():
        global _inotify_fd, _selector

        while 1:
            try:
                # wait before reading; give kernel time to write events
                time.sleep(delay)
                event_buffer = os.read(_inotify_fd, event_buffer_len)
                for event in _parse_events(event_buffer):
                    _dispatch_event(event)
            except BlockingIOError:
                time.sleep(0.001)
                continue
            except OSError:
                raise
            break
    return _read


def _parse_events(event_buffer):
    """Parses a buffer for inotify events.
    """
    logger.debug('parsing event buffer: {} ({})'
                 .format(event_buffer, len(event_buffer)))
    i = 0
    eventsz = ffi.sizeof('struct inotify_event')
    while i + eventsz <= len(event_buffer):
        wd, mask, cookie, length = struct.unpack_from('iIII', event_buffer, i)
        i += struct.calcsize('iIII')
        filename = event_buffer[i:i + length].rstrip(b'\0')
        i += length
        yield Event(wd, mask, cookie,
                    filename.decode())


def _dispatch_event(event):
    global _eventq
    logger.debug("dispatch event={}".format(event))
    asyncio.ensure_future(_eventq.put(event))


async def _dispatch():
    global _eventq

    logger.debug("eventq={}".format(_eventq))

    # TODO: add more details maybe?
    num_events = 0
    while 1:
        try:
            event = await _eventq.get()
            logger.debug("got event={!r}".format(event))
            num_events += 1
            result = _handle_event(event)
            logger.debug("handled result={!r}".format(result))
            _eventq.task_done()
        except asyncio.CancelledError:
            logger.debug("Dispatch cancelled.")
            break

    return {"num_events": num_events}


def _handle_event(event):
    """Pass the event to the handler.
    """
    global logger

    result = None

    # TODO: here we can match a quit event and then
    # raise asyncio.CancelledError

    if event.is_virtual:
        logger.debug("virtual event={!r}".format(event))
        future = asyncio.ensure_future(event.vhandler(event))
        result = (event, future)
    elif event.overflowed:
        # We have passed the upper limit for a inotify instance.
        # /proc/sys/fs/inotify/max_queued_events
        logger.warning("Event queue has overflowed (IN_Q_OVERFLOW) "
                       "max_queued_events={}"
                       .format(settings['max_queued_events']))
        # wd is -1 for this event so just continue
    elif event.ignored:
        logger.debug('ignored event={}'
                     .format(event))
        _delete_watchers(event.wd)
    elif event.unmounted:
        logger.debug('unmounted event={}'
                     .format(event))
        _delete_watchers(event.wd)
    else:
        watchers = _watchers.get(event.wd)

        if not watchers:
            # we have no handlers for a watch descriptor for some reason
            raise HandlerNotFoundError(event)

        first = watchers[0]

        assert all(watcher.path == first.path
                   for watcher in _watchers[event.wd]), "all watchers "
        "with the same wd must have the same path"

        path = Path(first.path)

        # A handler can be associated with multiple filesystem objects.
        # We need to specify which object this particular Event is about.
        if event.filename:
            event.path = path / event.filename
        else:
            # If we are watching a non-directory, we need to set filename
            event.filename = path.name
            event.path = path

        if event.relocated:
            # NOTE: The filename and path are the original filename and path
            # We cannot know where the file was relocated solely from events.
            # The user must call remove_watchers(event.path) to stop handling.
            # To know the real name the user could store the fd
            logger.debug('relocated: {}'.format(event))
        elif event.disappeared:
            # NOTE: In this case, inotify will also remove the watch
            # descriptor.
            logger.debug('disappeared: {}'.format(event))
        elif event.moved_from:
            logger.debug('moved_from: {}'.format(event))
            event.source = event.path
            _add_move_event(event)
        elif event.moved_into:
            logger.debug('moved_into: {}'.format(event))
            event.destination = event.path
            _add_move_event(event)
        elif event.created and event.is_directory:
            for watcher in (w for w in watchers if w.recursive):
                _copy_watcher(watcher, event.path)

        handlers = [watcher.handler(event)
                    for watcher in _watchers[event.wd]
                    if event.flags & watcher.flags]

        future = asyncio.ensure_future(asyncio.wait(handlers))
        result = (event, future)

    return result


def run(*, event_buffer_len=65536, read_delay=0.1):
    """Run event loop forever reading events from inotify.
    """
    global _watchers, _inotify_fd, logger

    if _inotify_fd < 0:
        _initialize()

    logger.debug('Running {}'.format(__name__))
    loop = asyncio.get_event_loop()
    loop.add_reader(_inotify_fd, _make_reader(event_buffer_len, read_delay))
    dispatch = asyncio.ensure_future(_dispatch())

    try:
        loop.run_until_complete(dispatch)
    except KeyboardInterrupt as e:
        logger.debug("Caught user interrupt.")
        dispatch.cancel()
        logger.debug("Completing pending events.")
        loop.run_forever()
        dispatch.exception()
    finally:
        logger.debug('Results: {!r}'.format(dispatch.result()))
        logger.debug('Stopping {}. Closing inotify file descriptor.'
                     .format(__name__))
        os.close(_inotify_fd)
        loop.close()

    return dispatch.result()
