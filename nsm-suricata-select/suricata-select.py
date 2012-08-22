#! /usr/bin/env python
#
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

    links = (
        ("bin/suricata%s" % (version), "bin/suricata"),
        ("bin/suricata-debug%s" % (version), "bin/suricata-debug"),
        )
        
    for (src, dst) in links:
        src = "%s/%s" % (NSM_PREFIX, src)
        dst = "%s/%s" % (NSM_PREFIX, dst)

        print "Linking %s -> %s" % (dst, src)

        if os.path.exists(dst) or os.path.islink(dst):
            os.unlink(dst)

        os.symlink(src, dst)

def main():

    action = None
    if_not_set = False

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "lh", ["help", "list", "if-not-set"])
    except getopt.GetoptError, e:
        usage(sys.stderr)
        return 1
    for o, a in opts:
        if o in ["-h", "--help"]:
            usage(sys.stdout)
            return 1
        elif o in ["-l", "--list"]:
            action = "list"
        elif o == "--if-not-set":
            if_not_set = True

    if not action and not args:
        return list_versions()
    elif action == "list":
        return list_versions()
    else:
        set_link(args[0], if_not_set=if_not_set)

sys.exit(main())
