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

from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_source("_inotify",
                      r"""
                        #include <sys/inotify.h>
                      """, libraries=[])
ffibuilder.cdef("""
struct inotify_event {
    int wd;
    ...;
};
int inotify_init(void);
int inotify_init1(int flags);
int inotify_add_watch(int fd, const char *pathname, uint32_t mask);
int inotify_rm_watch(int fd, int wd);

#define EMFILE ...
#define ENFILE ...

#define IN_ACCESS  ... /* File was accessed */
#define IN_MODIFY  ... /* File was modified */
#define IN_ATTRIB  ... /* Metadata changed */
#define IN_CLOSE_WRITE  ... /* Writtable file was closed */
#define IN_CLOSE_NOWRITE ... /* Unwrittable file closed */
#define IN_OPEN   ... /* File was opened */
#define IN_MOVED_FROM  ... /* File was moved from X */
#define IN_MOVED_TO  ... /* File was moved to Y */
#define IN_CREATE  ... /* Subfile was created */
#define IN_DELETE  ... /* Subfile was deleted */
#define IN_DELETE_SELF  ... /* Self was deleted */
#define IN_MOVE_SELF  ... /* Self was moved */

/* the following are legal events.  they are sent as needed to any watch */
#define IN_UNMOUNT  ... /* Backing fs was unmounted */
#define IN_Q_OVERFLOW  ... /* Event queued overflowed */
#define IN_IGNORED  ... /* File was ignored */

/* helper events */
#define IN_CLOSE  ... /* close */
#define IN_MOVE   ... /* moves */

/* special flags */
#define IN_ONLYDIR  ... /* only watch the path if it is a directory */
#define IN_DONT_FOLLOW  ... /* don't follow a sym link */
#define IN_EXCL_UNLINK  ... /* exclude events on unlinked objects */
#define IN_MASK_ADD  ... /* add to the mask of an already existing watch */
#define IN_ISDIR  ... /* event occurred against dir */
#define IN_ONESHOT  ... /* only send event once */

/*
 * All of the events - we build the list by hand so that we can add flags in
 * the future and not break backward compatibility.  Apps will get only the
 * events that they originally wanted.  Be sure to add new events here!
 */
#define IN_ALL_EVENTS ...
/* Flags for sys_inotify_init1.  */
#define IN_CLOEXEC ...
#define IN_NONBLOCK ...
""")

if __name__ == '__main__':
    ffibuilder.compile(tmpdir="build", verbose=True)
