#!/usr/bin/env python
import argparse
import os
import fnmatch
import shutil


def move_cot_langs(path, source, destination):
    "Renames language files and changes language codes"

    fname_pattern = '*.%s.lang.php' % source
    old_postfix = '.%s.lang.php' % source
    new_postfix = '.%s.lang.php' % destination

    # Rename the files
    for root, dirs, files in os.walk(path):
        langfiles = fnmatch.filter(files, fname_pattern)
        for fname in langfiles:
            new_name = fname.replace(old_postfix, new_postfix)
            old_file = os.path.join(root, fname)
            new_file = os.path.join(root, new_name)
            print "%s -> %s" % (fname, new_name)
            shutil.move(old_file, new_file)

    # Rename a directory in lang folder
    old_path = os.path.join(path, 'lang', source)
    new_path = os.path.join(path, 'lang', destination)
    print "%s -> %s" % (old_path, new_path)
    shutil.move(old_path, new_path)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Changes language code for\
        Cotonti language files.")
    p.add_argument('path', help="Path to directory tree containing langfiles")
    p.add_argument('source', help="Source language code")
    p.add_argument('destination', help="Destination language code")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.path):
        print "Path does not exist: %s" % arguments.source
        return 1

    if not arguments.source or not arguments.destination:
        print "Source and destination codes must not be empty"
        return 1

    if arguments.source is arguments.destination:
        print "Source and destination codes must be different"
        return 1

    move_cot_langs(arguments.path, arguments.source, arguments.destination)


if __name__ == '__main__':
    main()
