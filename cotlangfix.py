#!/usr/bin/env python
import argparse
import os
import fnmatch
import re

# Regexes for problem detection
has_array = re.compile(r'\$L\[["\']\w+["\']\]\s*=\s*array\(', re.I)
has_array_ignore = re.compile(r'\$L\[["\']\w+["\']\]\s*=\s*array\([\)\$]', re.I)
has_ls_array = re.compile(r'\$Ls\[["\']\w+["\']\]\s*=\s*array\(', re.I)
has_ext_cat = re.compile(r'\$L\[["\']ext_cat["\']\]\[')
has_multi_index = re.compile(r'\$\w+\[["\']\w+["\']\]\[')
has_multi_lines1 = re.compile(r'=\s*("|\'|<<<)')
has_multi_lines2 = re.compile(r'("|\');(\s*//.+)?\s*$')
has_multi_lines3 = re.compile(r'("|\')\);(\s*//.+)?\s*$')
has_cfg_params = re.compile(r'\$L\[["\'](cfg_\w+_params)["\']\]\s*=\s*'
                            r'array\(', re.I)


def detect_problems(file_name):
    "Checks if the file has problematic lang strings"

    problem_count = 0

    with open(file_name) as f:
        line_num = 1
        for line in f:
            if has_array.search(line) and not has_array_ignore.search(line):
                problem_count += 1

            if has_ls_array.search(line):
                problem_count += 1

            if has_multi_index.search(line):
                problem_count += 1

            if has_multi_lines1.search(line)\
               and not has_multi_lines2.search(line)\
               and not has_multi_lines3.search(line):
                problem_count += 1

            line_num += 1

    return problem_count

# Regexes to fix the problems
fix_cfg_params = re.compile(r'\$L\[["\'](cfg_\w+_params)["\']\]\s*=\s*'
                            r'array\(["\'](.*)["\']\);\s*$', re.I)
fix_cfg_params2 = re.compile(r'["\']\s*,\s*["\']')
fix_array1 = re.compile(r'\$L\[["\'](\w+)["\']\]\s*='
                        r'\s*array\(("|\')(.+?)\2,\s*("|\')(.*?)\4\);', re.I)
fix_array2 = re.compile(r'\$L\[["\'](\w+)["\']\]\s*='
                        r'\s*array\(("|\')(.+?)\2\);', re.I)
fix_ls_array = re.compile(r'\$Ls\[["\'](\w+)["\']\]\s*='
                          r'\s*array\(("|\')(.+?)\2,\s*("|\')(.+?)\4'
                          r'(,\s*("|\')(.+?)\7)?\);', re.I)
fix_multi_index = re.compile(r'\$(\w+)\[["\'](\w+)["\']\]\[["\']([\w-]+)["\']\]'
                             r'\s*=\s*(.+)')


def fix_lang_file(file_name, dest_name):
    "Fixes a language file if necessary"

    fixed_count = 0

    new_contents = ''

    with open(file_name) as f:
        line_num = 1
        for line in f:
            if has_cfg_params.search(line):
                # Contains a parameters entry
                # Check if the array is complete in this line
                m = fix_cfg_params.search(line)
                if m:
                    # Inline array, we can merge it
                    items = fix_cfg_params2.split(m.group(2))
                    items_str = ',' . join(items)

                    line = "$L['%s'] = '%s';\n" % (m.group(1), items_str)

                    fixed_count += 1

                else:
                    # Multiline entries should be fixed manually
                    print "Please join params array manually in %s at line %d:\n%s"\
                          % (file_name, line_num, line)

            elif has_array.search(line) and not has_array_ignore.search(line):
                # Array entry needs fixing

                m = fix_array1.search(line)
                if m:
                    # Array entry with 2 items

                    line = """$L['%(key)s'] = %(q1)s%(val1)s%(q1)s;
$L['%(key)s_hint'] = %(q2)s%(val2)s%(q2)s;
""" % {'key': m.group(1),
       'q1': m.group(2), 'val1': m.group(3),
       'q2': m.group(4), 'val2': m.group(5)}

                    fixed_count += 1

                else:
                    m = fix_array2.search(line)
                    if m:
                        # Array entry with 1 item

                        line = """$L['%(key)s'] = %(q1)s%(val1)s%(q1)s;
""" % {'key': m.group(1),
       'q1': m.group(2), 'val1': m.group(3)}

                        fixed_count += 1

                    else:
                        # Error
                        print "Could not fix line %d in %s:\n%s"\
                            % (line_num, file_name, line)

            elif has_ls_array.search(line):
                # $Ls entry for plurals/declension

                m = fix_ls_array.search(line)
                if m:
                    line = "$Ls['%s'] = \"%s,%s" % (m.group(1), m.group(3),
                                                    m.group(5))
                    if m.group(6):
                        line += ",%s" % m.group(8)
                    line += "\";\n"

                    fixed_count += 1

                else:
                    # Error
                    print "Could not fix line %d in %s:\n%s"\
                          % (line_num, file_name, line)

            elif has_multi_index.search(line):
                # Multi index entry needs fixing

                m = fix_multi_index.search(line)
                if m:
                    line = """$%(var)s['%(key1)s_%(key2)s'] = %(tail)s
""" % {'var': m.group(1), 'key1': m.group(2),
       'key2': m.group(3), 'tail': m.group(4)}
                    # print line
                    fixed_count += 1
                else:
                    # Error
                    print "Could not fix line %d in %s:\n%s"\
                          % (line_num, file_name, line)

            elif has_multi_lines1.search(line)\
                and not has_multi_lines2.search(line)\
                    and not has_multi_lines3.search(line):
                # Multiline entries should be fixed manually
                print "Please join multiline entry manually in %s at line %d:\n%s"\
                      % (file_name, line_num, line)

            new_contents += line
            line_num += 1

    dest_dir = os.path.dirname(dest_name)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_name, 'w') as f:
        f.write(new_contents)

    return fixed_count


def fix_lang_files(source, destination):
    "Walks the directory tree and fixes all langfiles it finds"

    problem_count = 0
    file_count = 0
    fixed_count = 0
    fixed_files = 0

    for root, dirs, files in os.walk(source):
        langfiles = fnmatch.filter(files, '*.lang.php')
        if len(langfiles) > 0:
            subdir = root.replace(os.path.join(source, ''), '')
            new_dir = os.path.join(destination, subdir)
            for fname in langfiles:
                file_name = os.path.join(root, fname)
                count = detect_problems(file_name)
                if count > 0:
                    problem_count += count
                    file_count += 1
                    dest_name = os.path.join(new_dir, fname)
                    count = fix_lang_file(file_name, dest_name)
                    if count > 0:
                        fixed_count += count
                        fixed_files += 1

    print "Found %d problems in %d files" % (problem_count, file_count)
    print "Fixed %d problems in %d files" % (fixed_count, fixed_files)


def main():
    "Runs as command line program"

    p = argparse.ArgumentParser(description="Updates Cotonti language files\
        and makes them compatible with Transifex.")
    p.add_argument('source', help="Path where langfiles should be searched\
        and modified")
    p.add_argument('destination', default='', nargs='?',
                   help="Path where result files are stored."
                        "Source files are modified if this is omitted.")

    arguments = p.parse_args()

    if not os.path.isdir(arguments.source):
        print "Path does not exist: %s" % arguments.source
        return 1

    if arguments.destination and not os.path.isdir(arguments.destination):
        os.makedirs(arguments.destination)

    destination = arguments.destination if arguments.destination\
        else arguments.source

    fix_lang_files(arguments.source, destination)


if __name__ == '__main__':
    main()
