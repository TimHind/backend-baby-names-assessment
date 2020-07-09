#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BabyNames python coding exercise.
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
import sys
import re
import argparse

def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    with open(filename) as f:
        text = f.read()
    names = []
    pattern = r'Popularity in (\d\d\d\d)'
    year_match = re.search(pattern, text)
    if year_match is None:
        return None
    year = year_match.group(1)
    names.append(year)
    pattern = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'
    names_ranks = re.findall(pattern, text)
    names_to_rank = {}
    for rank_tuple in names_ranks:
        rank, boy_name, girl_name = rank_tuple
        if boy_name not in names_to_rank:
            names_to_rank[boy_name] = rank
        if girl_name not in names_to_rank:
            names_to_rank[girl_name] = rank
    sorted_names = sorted(names_to_rank.items())
    for name, rank in sorted_names:
        names.append(f"{name} {rank}")
    return names

def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser

def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)
    if not ns:
        parser.print_usage()
        sys.exit(1)
    file_list = ns.files
    # option flag
    create_summary = ns.summaryfile
    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).
    for filename in file_list:
        names = extract_names(filename)
        text = '\n'.join(names)
        if create_summary:
            with open(f'{filename}.summary', 'w') as f:
                f.write(text)
        else:
            print(text)
if __name__ == '__main__':
    main(sys.argv[1:])