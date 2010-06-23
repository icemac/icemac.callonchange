# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import fsevents
import subprocess
import sys
import time


def print_usage():
    print "USAGE: callonchange <path> <binary>"
    print "Calls the <binary> when the <path> or something in it changes."


def callbackFactory(*params):

    def callback(subpath, mask):
        try:
            subprocess.Popen(params)
        except OSError, e:
            print "OSError %s %s" % e.args
            print "Popen params where: ",
            print params
            sys.exit(-1)
    return callback

class Observer(object):

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


def mangle_call_args(path, params, argv):

    argv.reverse()

    if path is None:
        try:
            path = argv.pop()
        except IndexError:
            print_usage()
            return None, None
    if params is None:
        try:
            params = argv.pop()
        except IndexError:
            print_usage()
            return None, None
    if isinstance(params, basestring):
        params = [params]
    if len(argv):
        params.extend(reversed(argv))
    return path, params


def callonchange(path="src", params="bin/test"):

    args = sys.argv[1:]

    path, params = mangle_call_args(path, params, args)
    if (path, params) != (None, None):
        observer = Observer(path, params)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
