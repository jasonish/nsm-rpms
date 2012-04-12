#! /usr/bin/env python

import sys
import getopt
import os
import os.path
import re
import shutil

dist_path_map = {"el6": "el/6",
                 "fc16": "fedora/16",
                 }

basearch = {"x86_64": "x86_64",
            "i686": "i386",
            }

def main():

    repo_root = None
    deploy_arch = None
    deploy_dist = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "", ["repo-root=", "arch=", "dist="])
    except getopt.GetoptError, err:
        print >>sys.stderr, "ERROR: Bad command line parameter."
        return 1
    for o, a in opts:
        if o == "--repo-root":
            repo_root = a
        elif o == "--dist":
            deploy_dist = a
        elif o == "--arch":
            deploy_arch = a

    if not repo_root:
        print >>sys.stderr, "ERROR: --repo-root required"
        return 1
    if not deploy_arch:
        print >>sys.stderr, "ERROR: --arch required"
        return 1
    if not deploy_dist:
        print >>sys.stderr, "ERROR: --dist required"
        return 1

    if not os.path.exists(repo_root):
        print >>sys.stderr, "ERROR: %s does not exist." % (repo_root)

    for filename in args:
        m = re.search(".*\.(.*)\.(.*)\.rpm", filename)
        if not m:
            print "WARNING: %s does not look like a valid RPM." % (
                filename)
            continue
        dist = m.group(1)
        arch = m.group(2)

        if deploy_dist and deploy_dist != dist:
            print("Skipping %s." % (filename))
            continue
        if arch not in ["noarch", "src"] and \
                deploy_arch and deploy_arch != arch:
            print("Skipping %s." % (filename))
            continue

        if dist not in dist_path_map:
            print("ERROR: Unknown dist: %s" % (dist))
            return 1

        dist_path = dist_path_map[dist]

        if arch == "src":
            dst = "%s/%s/SRPMS" % (repo_root, dist_path)
        elif arch in ["noarch", deploy_arch]:
            dst = "%s/%s/%s" % (repo_root, dist_path, basearch[deploy_arch])
            
        if filename.find("debuginfo") >= 0:
            dst += "/debug"

        print("Deploying %s to %s" % (os.path.basename(filename), dst))
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutil.copy(filename, dst)

sys.exit(main())
