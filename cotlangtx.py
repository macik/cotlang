#!/usr/bin/env python
import argparse
import os
import fnmatch
import re


def grab_lang_resources(path):
    "Grabs langfiles and prints txconfig resources"

    registered_resources = []

    for root, dirs, files in os.walk(path):
        langfiles = fnmatch.filter(files, '*.en.lang.php')
        subdir = root.replace(os.path.join(path, ''), '').replace('\\', '/')
        subdir_root = subdir.split('/')[0]
        subdir_filter = re.sub(r'\ben\b', '<lang>', subdir)
        for fname in langfiles:
            # Make unique resource name
            base_name = fname.replace('.en.lang.php', '')
            res_name = subdir_root + '_' + base_name

            # Calculate config vars
            source_file = subdir + '/' + fname
            source_filter = subdir_filter + '/' + base_name + '.<lang>.lang.php'

            source_entry = """[cotonti.%s]
source_file = %s
file_filter = %s
source_lang = en
type = PHP_ALT_ARRAY
""" % (res_name, source_file, source_filter)

            print source_entry

            # Add to registry to avoid repeats
            registered_resources.append(res_name)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Generates Transifex config resources\
        based on language files in target directory and prints them on screen.")
    p.add_argument('path', default='.', help="Path to directory with lang files")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.path):
        print "Path does not exist: %s" % arguments.path
        return 1

    grab_lang_resources(arguments.path)


if __name__ == '__main__':
    main()
