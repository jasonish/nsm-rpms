#! /usr/bin/env python

import sys
import os

repo_dirs = [
    "SRPMS",
    "i386",
    "i386/debug",
    "x86_64",
    "x86_64/debug",
]

def is_repo_dir(directory):
    return len([d for d in repo_dirs if directory.endswith(d)]) > 0

def main():

    for root, dirs, files in os.walk(sys.argv[1]):

        if is_repo_dir(root):
            print("Updating repo %s." % (root))
            os.system("createrepo --database --exclude debug/*.rpm --update %s" % (root))

    return 0

sys.exit(main())
