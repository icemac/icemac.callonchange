# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import fsevents
import optparse
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
            # On error it would be nice to have a hint why it failed:
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
        # as told by MacFSEvents
        callback = callbackFactory(*self.params)
        self.observer = fsevents.Observer()
        self.observer.start()
        self.stream = fsevents.Stream(callback, self.path)
        self.observer.schedule(self.stream)

    def stop(self):
        self.observer.unschedule(self.stream)
        self.observer.stop()




def mangle_call_args(args, argv):
    "Combine buildout and sys.argv parameters into one list."
    call_args = list(tuple(args) + tuple(argv))

    parser = optparse.OptionParser(
        usage="%prog [options] path action [action options]")
    parser.add_option(
        "-e", action="append", dest="extensions", default=[],
        help="only call action on changes of a file with this extension "\
             "(option might be used multiple times)")
    parser.disable_interspersed_args()

    (options, parsed_args) = parser.parse_args(call_args)

    if len(parsed_args) < 2:
        print USAGE
        return None, None, None

    return parsed_args[0], parsed_args[1:], options.extensions
