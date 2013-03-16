#!/usr/bin/env python
import argparse
import os
import fnmatch


def utime_cot_langs(path, lang):
    "Updates modification time for langfiles with specific code"

    fname_pattern = '*.%s.lang.php' % lang

    for root, dirs, files in os.walk(path):
        langfiles = fnmatch.filter(files, fname_pattern)
        for fname in langfiles:
            old_file = os.path.join(root, fname)
            print "Mod %s" % fname
            os.utime(old_file, None)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Updates modification time for\
        specific Cotonti locale from source tree, so Transifex can push them.")
    p.add_argument('path', help="Path to directory tree containing langfiles")
    p.add_argument('lang', help="Language code")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.path):
        print "Path does not exist: %s" % arguments.path
        return 1

    if not arguments.lang:
        print "Language code must not be empty"
        return 1

    utime_cot_langs(arguments.path, arguments.lang)


if __name__ == '__main__':
    main()
