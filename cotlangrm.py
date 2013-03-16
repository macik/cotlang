#!/usr/bin/env python
import argparse
import os
import fnmatch


def rm_cot_langs(path, lang):
    "Removes language files for a specific code"

    fname_pattern = '*.%s.lang.php' % lang

    # Remove language files
    for root, dirs, files in os.walk(path):
        langfiles = fnmatch.filter(files, fname_pattern)
        for fname in langfiles:
            old_file = os.path.join(root, fname)
            print "Remove %s" % fname
            os.remove(old_file)

    # Remove directory in lang folder
    old_path = os.path.join(path, 'lang', lang)
    print "Remove %s" % old_path
    os.rmdir(old_path)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Removes files for\
        specific Cotonti locale from source tree.")
    p.add_argument('path', help="Path to directory tree containing langfiles")
    p.add_argument('lang', help="Language code")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.path):
        print "Path does not exist: %s" % arguments.path
        return 1

    if not arguments.lang:
        print "Language code must not be empty"
        return 1

    rm_cot_langs(arguments.path, arguments.lang)


if __name__ == '__main__':
    main()
