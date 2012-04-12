#! /usr/bin/env python

import sys
import os

def main():

    for root, dirs, files in os.walk(sys.argv[1]):
        rpm_count = len(filter(lambda f: f.endswith(".rpm"), files))
        if rpm_count:
            print("Updating repo %s." % (root))
            os.system("createrepo --database --unique-md-filenames --exclude debug/*.rpm --update %s" % (root))

    return 0

sys.exit(main())
