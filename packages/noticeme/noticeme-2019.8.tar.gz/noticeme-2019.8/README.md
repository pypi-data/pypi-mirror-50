# noticeme

Provides python bindings for inotify and framework for building file watchers using coroutines.

Please note this only runs on Linux and a have no plans to support any other OS.

There are many, many alternatives though.

noticeme includes the noticeme command for quickly setting up a file watcher.

## Using noticeme declaratively

If you just need a small file watcher you can try this out.

```
pip install --user noticeme # install
nano noticeme.cfg # use noticeme/examples/noticeme.cfg for an example
noticeme # start watching
```

To see a full list of events:

```
  noticeme events
```

To select which watchers we want to run we can give a list.\
Say we had watchers named build:js, build:css, and test in a single config file.\
In one terminal we could run:

```
  noticeme build:js build:css
```

And in another:

```
  noticeme test
```


## Quick look at configuration

see noticeme/examples/noticeme.cfg for details

```
# noticeme.cfg
[should]
  clear_screen = yes

[imports]
  example = A .py file with a @noticeme.watcher decorator in it

[my_watcher]
  description = This is an example.
  paths = . **
  events = written
  regex = ^docs
  glob = *.txt
  shell = echo "my_watcher: file was added"
```

## Using noticeme to build a file watcher programmatically

```
import asyncio
import noticeme

@noticeme.watcher('/path/to/directory', 'created modified')
async def my_watcher(event):
  if '.py' == event.path.suffix.lower():
    proc = await asyncio.create_subprocess_exec('cmd', event.path.absolute())
    await proc.wait()

if __name__ == '__main__':
  noticeme.run()
```

## Requirements

- Linux >= 2.6.13
- Python >= 3.5
- cffi
- C compiler installed (if you need to run inotify_build.py)

## Install

### pip

```
pip install --user noticeme
```

### Include directly

- Copy noticeme.py and inotify_build.py to your project directory
- Within noticeme's package directory run:

```
python3 inotify_build.py
```

- This creates a 'build' directory containing the result of ffibuilder.compile
- You should now be able to use noticeme.
- inotify_build.py will no longer be needed.

## Alternatives

[watchdog](https://github.com/gorakhargosh/watchdog)
[pyinotify](https://github.com/seb-m/pyinotify)

## Version 2019.7

- set a more informative window title

## Version 2019.8

- add '.noticeme' as possible config file
