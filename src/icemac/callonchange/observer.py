# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import atexit
import fsevents
import optparse
import os.path
import pkg_resources
import subprocess
import sys
import thread


def run_subprocess(quite, params):
    """Run `params` in a subprocess."""
    if not quite:
        print "Calling: %s" % " ".join(params)
    try:
        subprocess.Popen(params)
    except OSError, e:
        # On error it would be nice to have a hint why it failed:
        print "OSError: [Errno %s] %s" % e.args
        if  quite:
            print "Parameters were: %s" % " ".join(params)
        # Exit the observer on error.
        sys.exit(-1)


def run_subprocess_from_thread(quite, params):
    """Run `params` in a subprocess if current thread is not the main one."""
    try:
        run_subprocess(quite, params)
    except SystemExit:
        # Signal the process to exit as we are in a thread here.
        thread.interrupt_main()


def directoryCallbackFactory(quite, *params):
    """Create callback function for directory events."""
    def callback(subpath, mask):
        # Subpath and mask of changes do not matter here. There is
        # currently no way (and no desire) to handle them over to the
        # subprocess.
        run_subprocess_from_thread(quite, params)
    return callback


def fileCallbackFactory(extensions, quite, *params):
    """Create callback function for file events."""
    def callback(event):
        # event.name contains the absolute path to the changed file
        path, ext = os.path.splitext(event.name)
        if ext in extensions:
            # Only run process when extension of changed file is in
            # the list of observed file types
            run_subprocess_from_thread(quite, params)
    return callback


class Observer(object):
    """Observer for path."""

    extensions = []  # only call utility when a file with this ext changed
    quite = False  # when True, do not print any non-error output
    immediate = False  # run immediately after invocation

    def __init__(self, path, params, **options):
        self.path = path
        self.params = params
        self._is_running = False
        for key, value in options.items():
            setattr(self, key, value)

    def start(self):
        if self.immediate:
            run_subprocess(self.quite, self.params)
        if self.extensions:
            # observe explicit file extensions
            callback = fileCallbackFactory(
                self.extensions, self.quite, *self.params)
        else:
            # observe everything in the directory
            callback = directoryCallbackFactory(self.quite, *self.params)
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
    """Combine buildout and sys.argv parameters into one list."""
    call_args = list(tuple(args) + tuple(argv))

    parser = optparse.OptionParser(
        usage="%prog [options] path utility [utility arguments]",
        version=pkg_resources.get_distribution('icemac.callonchange').version)
    parser.description = (
        "%prog invokes <utility> with its <utility arguments> when <path> or "
        "something in it changes.")
    parser.add_option(
        "-e", action="append", metavar="EXTENSION", dest="extensions",
        default=[],
        help="only call utility on changes of a file with this extension "\
             "(option might be used multiple times)")
    parser.add_option(
        "-q", action="store_true", dest="quite", default=False,
        help=("Do not display any output of callonchange. "
              "(Still displays the output of the utility.)"))
    parser.add_option(
        "-i", action="store_true", dest="immediate", default=False,
        help=("Run utility immediately after callonchange has been started."
              "(By default the utility is only run when something changed.)"))
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
    for ext in options.extensions:
        if not ext.startswith('.'):
            ext = '.' + ext
        extensions.append(ext)
    options.extensions = extensions

    return parsed_args[0], parsed_args[1:], options.__dict__
