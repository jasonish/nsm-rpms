#! /usr/bin/env python

# Copyright (c) 2012 Jason Ish <ish@unx.ca>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

    -l,--list       List available versions
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

    # New style.
    for directory in os.listdir("%s/packages/snort" % (NSM_PREFIX)):
        versions.append(directory)

    return versions

def is_active(version):
    snort = "%s/bin/snort" % (NSM_PREFIX)
    if os.path.exists(snort):
        if version in os.readlink(snort).split("/"):
            return True

    # Maybe an older style package.
    if os.path.basename(os.readlink(snort)) == "snort%s" % (version):
        return True

    return False

def list_versions():
    versions = get_versions()
    if not versions:
        print("no versions of snort installed")
    else:
        for version in versions:
            if is_active(version):
                print("%s (active)" % (version))
            else:
                print("%s" % (version))
        
def set_link(version, if_not_set=False, additional_prefixes=[]):

    versions = get_versions()

    if version not in versions:
        err(1, "%s is not not installed" % (version))

    # If if_not_set is True and we already have a link, don't do anything.
    if if_not_set and os.path.exists("%s/bin/snort" % (NSM_PREFIX)):
        sys.exit(0)

    if os.path.exists("%s/packages/snort/%s" % (NSM_PREFIX, version)):
        new_set_link(version, additional_prefixes)
    else:
        old_set_link(version, additional_prefixes)

def new_set_link(version, additional_prefixes):
    links = ("bin/snort",
             "bin/u2boat",
             "bin/u2spewfoo",
             "lib/snort",
             "lib/snort_dynamicengine",
             "lib/snort_dynamicpreprocessor",
             "share/man/man8/snort.8",
             )

    # Remove existing links.
    for link in links:
        path = "%s/%s" % (NSM_PREFIX, link)
        if os.path.exists(path) or os.path.islink(path):
            print("Unlinking %s." % (path))
            os.unlink(path)

    # Create new links.
    for link in links:
        src = "%s/packages/snort/%s/%s" % (NSM_PREFIX, version, link)
        dst = "%s/%s" % (NSM_PREFIX, link)
        print("Linking %s -> %s." % (dst, src))
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        os.symlink(src, dst)

    # Link additional prefixes.
    for prefix in additional_prefixes:
        for link in links:
            src = "%s/%s" % (NSM_PREFIX, link)
            dst = "%s/%s" % (prefix, link)
            print("Linking %s -> %s." % (dst, src))
            if os.path.islink(dst):
                os.unlink(dst)
            elif os.path.exists(dst):
                print("WARNING: %s is not link.  Not removing.")
                continue
            os.symlink(src, dst)

def old_set_link(version, additional_prefixes):
    # Remove existing symlinks.
    paths = ["%s/bin/snort" % (NSM_PREFIX),
             "%s/lib/snort_dynamicengine" % (NSM_PREFIX),
             "%s/lib/snort_dynamicpreprocessor" % (NSM_PREFIX)]
    for p in paths:
        if os.path.exists(p):
            os.unlink(p)

    for dst in paths:
        src = dst.replace("snort", "snort%s" % (version))
        if os.path.exists(dst) or os.path.islink(dst):
            os.unlink(dst)
        os.symlink(src, dst)

    for prefix in additional_prefixes:
        for src in paths:
            dst = src.replace(NSM_PREFIX, prefix)
            if os.path.exists(dst):
                if os.path.islink(dst):
                    os.unlink(dst)
                else:
                    print >>sys.stderr, \
                        "ERROR: %s exists and is not a symlink. " \
                        "It will not be replaced." % (dst)
            os.symlink(src, dst)

def main():

    action = None
    if_not_set = False
    additional_prefixes = []

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "l", ["list", "if-not-set", "usrlocal"])
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

    if not args or action == "list":
        return list_versions()
    else:
        set_link(args[0],
                 if_not_set=if_not_set,
                 additional_prefixes=additional_prefixes)

sys.exit(main())
