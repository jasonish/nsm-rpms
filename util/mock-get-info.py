#! /usr/bin/env python

import sys
import getopt

def main():
    config_opts = {}

    config = None
    action = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", (
                ["config=", "dist", "arch"]))
    except getopt.GetoptError, err:
        print("ERROR: Invalid command line.")
        return 1
    for o, a in opts:
        if o == "--config":
            config = a
        elif o == "--dist":
            if action == None:
                action = "dist"
            else:
                print("ERROR: Only one of --arch and --dist may be specified.")
                return 1
        elif o == "--arch":
            if action == None:
                action = "arch"
            else:
                print("ERROR: Only one of --arch and --dist may be specified.")
                return 1

    if not config:
        print("ERROR: --config is required.")
        return 1
    if not action:
        print("ERROR: --arch or --dist must be specified.")
        return 1

    exec(open("/etc/mock/%s.cfg" % config).read())
    if action == "arch":
        print config_opts["target_arch"]
    elif action == "dist":
        print config_opts["dist"]
    else:
        return 1

sys.exit(main())
