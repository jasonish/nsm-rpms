#! /usr/bin/env python

import sys
import os.path
import os
import glob
import re
import getopt

NSM_PREFIX = "/opt/nsm"

def usage(outobj):

    print >>outobj, ("""
USAGE: %s [options] [version]

Options:

    --list          List available versions
    --if-not-set    Only set if not already set

""" % (sys.argv[0]))

def err(ec, msg):
    print >>sys.stderr, (msg)
    sys.exit(1)

def get_versions():

    versions = []

    for filename in glob.glob("%s/bin/suricata[0-9]*" % (NSM_PREFIX)):
        m = re.search("suricata([\d\.]+)$", filename)
        if m:
            versions.append(m.group(1))

    return versions

def list_versions():
    versions = get_versions()
    if not versions:
        print("no versions of suricata installed")
    else:
        for v in versions:
            print(v)
        
def set_link(version, if_not_set=False):
    versions = get_versions()
    if version not in versions:
        err(1, "%s is not not installed" % (version))

    # If if_not_set is True and we already have a link, don't do anything.
    if if_not_set and os.path.exists("%s/bin/suricata" % (NSM_PREFIX)):
        sys.exit(0)

    suricata_path = "%s/bin/suricata" % (NSM_PREFIX)
    if os.path.exists(suricata_path) or os.path.islink(suricata_path):
        os.unlink(suricata_path)
    src = "%s/bin/suricata%s" % (NSM_PREFIX, version)
    os.symlink(src, suricata_path)

    suricata_path = "%s/bin/suricata-debug" % (NSM_PREFIX)
    if os.path.exists(suricata_path) or os.path.islink(suricata_path):
        os.unlink(suricata_path)
    src = "%s/bin/suricata-debug%s" % (NSM_PREFIX, version)
    os.symlink(src, suricata_path)

def main():

    action = None
    if_not_set = False

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "h", ["help", "list", "if-not-set"])
    except getopt.GetoptError, e:
        usage(sys.stderr)
        return 1
    for o, a in opts:
        if o in ["-h", "--help"]:
            usage(sys.stdout)
            return 1
        elif o == "--list":
            action = "list"
        elif o == "--if-not-set":
            if_not_set = True

    if not action and not args:
        err(1, "nothing to do")
    elif action == "list":
        return list_versions()
    else:
        set_link(args[0], if_not_set=if_not_set)

sys.exit(main())
