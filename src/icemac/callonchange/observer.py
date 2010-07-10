# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import atexit
import fsevents
import optparse
import os.path
import subprocess
import sys
import time


def run_subprocess(params):
    "Run the given pramams in a subprocess."
    try:
        subprocess.Popen(params)
    except OSError, e:
        # On error it would be nice to have a hint why it failed:
        print "OSError: %s" % (e.args,)
        print "Popen params were: ",
        print params
        # Exit the observer on error.
        sys.exit(-1)



def directoryCallbackFactory(*params):
    "Create callback function for directory events."
    def callback(subpath, mask):
        # Subpath and mask of changes do not matter here. There is
        # currently no way (and no desire) to handle them over to the
        # subprocess.
        run_subprocess(params)
    return callback


def fileCallbackFactory(extensions, *params):
    "Create callback function for file events."
    def callback(event):
        # event.name contains the absolute path to the changed file
        path, ext = os.path.splitext(event.name)
        if ext in extensions:
            # Only run process when extension of changed file is in
            # the list of observed file types
            run_subprocess(params)
    return callback


class Observer(object):
    "Observer for path."
    def __init__(self, path, params, extensions):
        self.path = path
        self.params = params
        self.extensions = extensions
        self._is_running = False

    def start(self):
        if self.extensions:
            # observe explicit file extensions
            callback = fileCallbackFactory(self.extensions, *self.params)
        else:
            # observe everything in the directory
            callback = directoryCallbackFactory(*self.params)
        self.observer = fsevents.Observer()
        self.observer.start()
        file_events = bool(self.extensions)
        self.stream = fsevents.Stream(
            callback, self.path, file_events=file_events)
        self.observer.schedule(self.stream)
        self._is_running = True
        atexit.register(self.stop)

    def stop(self):
        if self._is_running:
            self.observer.unschedule(self.stream)
            self.observer.stop()
            self._is_running = False


def mangle_call_args(args, argv):
    "Combine buildout and sys.argv parameters into one list."
    call_args = list(tuple(args) + tuple(argv))

    parser = optparse.OptionParser(
        usage="%prog [options] path utility [utility arguments]")
    parser.description = (
        "%prog invokes <utility> with its <utility arguments> when <path> or "
        "something in it changes.")
    parser.add_option(
        "-e", action="append", dest="extension", default=[],
        help="only call utility on changes of a file with this extension "\
             "(option might be used multiple times)")
    parser.disable_interspersed_args()

    (options, parsed_args) = parser.parse_args(call_args)

    # At least path and action are required, otherwise we print a
    # helpful message.
    if len(parsed_args) < 2:
        parser.print_help()
        return None, None, None

    # For convinience it is allowed to omit the leading dots in of the
    # specified extension, so they get added here, as they are needed
    # by the observer.
    extensions = []
    for ext in options.extension:
        if not ext.startswith('.'):
            ext = '.' + ext
        extensions.append(ext)

    return parsed_args[0], parsed_args[1:], extensions
