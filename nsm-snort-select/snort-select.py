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
    --usrlocal      Also setup links in /usr/local

""" % (sys.argv[0]))

def err(ec, msg):
    print >>sys.stderr, (msg)
    sys.exit(1)

def get_versions():

    versions = []

    for filename in glob.glob("%s/bin/snort*" % (NSM_PREFIX)):
        m = re.search("snort(\d+\.\d+\.\d+[\.\d]*)$", filename)
        if m:
            versions.append(m.group(1))

    return versions

def list_versions():
    versions = get_versions()
    if not versions:
        print("no versions of snort installed")
    else:
        for v in versions:
            print(v)
        
def set_link(version, if_not_set=False, additional_prefixes=[]):
    versions = get_versions()
    if version not in versions:
        err(1, "%s is not not installed" % (version))

    # If if_not_set is True and we already have a link, don't do anything.
    if if_not_set and os.path.exists("%s/bin/snort" % (NSM_PREFIX)):
        sys.exit(0)

    # Remove existing symlinks.
    paths = ["%s/bin/snort" % (NSM_PREFIX),
             "%s/lib/snort_dynamicengine" % (NSM_PREFIX),
             "%s/lib/snort_dynamicpreprocessor" % (NSM_PREFIX)]
    for p in paths:
        if os.path.exists(p):
            os.unlink(p)

    src = "%s/bin/snort%s" % (NSM_PREFIX, version)
    for prefix in [NSM_PREFIX] + additional_prefixes:
        dst = "%s/bin/snort" % (prefix)
        if os.path.islink(dst) or os.path.exists(dst):
            os.unlink(dst)
        os.symlink(src, dst)

    src = "%s/lib/snort%s_dynamicengine" % (NSM_PREFIX, version)
    for prefix in [NSM_PREFIX] + additional_prefixes:
        dst = "%s/lib/snort_dynamicengine" % (prefix)
        if os.path.islink(dst) or os.path.exists(dst):
            os.unlink(dst)
        os.symlink(src, dst)
    
    src = "%s/lib/snort%s_dynamicpreprocessor" % (NSM_PREFIX, version)
    for prefix in [NSM_PREFIX] + additional_prefixes:
        dst = "%s/lib/snort_dynamicpreprocessor" % (prefix)
        if os.path.islink(dst) or os.path.exists(dst):
            os.unlink(dst)
        os.symlink(src, dst)

def main():

    action = None
    if_not_set = False
    additional_prefixes = []

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "", ["list", "if-not-set", "usrlocal"])
    except getopt.GetoptError, e:
        usage(sys.stderr)
        return 1
    for o, a in opts:
        if o == "--list":
            action = "list"
        elif o == "--if-not-set":
            if_not_set = True
        elif o == "--usrlocal":
            additional_prefixes.append("/usr/local")

    if not action and not args:
        err(1, "nothing to do")
    elif action == "list":
        return list_versions()
    else:
        set_link(args[0],
                 if_not_set=if_not_set,
                 additional_prefixes=additional_prefixes)

sys.exit(main())
