#!/usr/bin/env python
import argparse
import os
import fnmatch
import shutil


def copy_cot_langs(source, destination, lang):
    "Copies Cotonti lang files from source tree to destination"

    fname_pattern = '*.lang.php' if lang is 'all' else '*.%s.lang.php' % lang

    for root, dirs, files in os.walk(source):
        langfiles = fnmatch.filter(files, fname_pattern)
        if len(langfiles) > 0:
            subdir = root.replace(os.path.join(source, ''), '')
            print "Copy %s" % subdir
            new_dir = os.path.join(destination, subdir)
            if not os.path.isdir(new_dir):
                os.makedirs(new_dir)
            for fname in langfiles:
                print "Copy %s" % os.path.join(subdir, fname)
                old_file = os.path.join(root, fname)
                new_file = os.path.join(new_dir, fname)
                shutil.copy(old_file, new_file)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Copies Cotonti language files\
        from one source tree to another. Overwrites existing files.")
    p.add_argument('source', help="Path to source directory tree")
    p.add_argument('destination', help="Path to destination directory tree")
    p.add_argument('-l', '--lang', default='all', help="Locale to copy")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.source):
        print "Path does not exist: %s" % arguments.source
        return 1

    if not os.path.isdir(arguments.destination):
        os.makedirs(arguments.destination)

    copy_cot_langs(arguments.source, arguments.destination, arguments.lang)


if __name__ == '__main__':
    main()
