# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import fsevents
import subprocess
import sys
import time

USAGE = """\
USAGE: callonchange <path> <command> [<arg1> <arg2> ...]
Calls <command> with <arg>s when <path> or something in it changes.
<command> can be a binary or a script.
"""


def callbackFactory(*params):
    "Create callback function."
    def callback(subpath, mask):
        try:
            subprocess.Popen(params)
        except OSError, e:
            print "OSError: %s" % (e.args,)
            print "Popen params were: ",
            print params
            sys.exit(-1)
    return callback

class Observer(object):
    "Observer for path."
    def __init__(self, path, params):
        self.path = path
        self.params = params

    def start(self):
        callback = callbackFactory(*self.params)
        self.observer = fsevents.Observer()
        self.observer.start()
        self.stream = fsevents.Stream(callback, self.path)
        self.observer.schedule(self.stream)

    def stop(self):
        self.observer.unschedule(self.stream)
        self.observer.stop()


def mangle_call_args(args, argv):
    "Mange buildout and sys.argv parameters into one list."
    args = tuple(args) + tuple(argv)
    if len(args) < 2:
        print USAGE
        return None, None
    return args[0], args[1:]


def callonchange(*args):
    "Main function which can handle buildout and sys.argv parameters."
    path, params = mangle_call_args(args, sys.argv[1:])
    if path is None:
        return
    observer = Observer(path, params)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
