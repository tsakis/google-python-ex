#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def get_year(html_string):
    year_m = re.search(r'Popularity in ([0-9]+)<', html_string)
    if year_m:
        year = year_m.group(1)
    else:
        year = "Unknown"
    return year

def get_name_values(html_string):
    pos_names = re.findall(r'<td>([0-9]+)</td><td>(\w+)</td><td>(\w+)</td>', html_string)

    names_dict = {}
    doubles = 0
    for tup in pos_names:
        num = tup[0]
        for name in tup[1:]:
            if name in names_dict:
                doubles += 1
            # the last instance will have the smallest value
            names_dict[name] = num
    assert int(num) * 2 == len(names_dict) + doubles, "Number of names don't add up!"
    return names_dict

def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    # +++your code here+++
    with open(filename, "r") as f:
        filestring = f.read()
        year = get_year(filestring)
        names_pos = get_name_values(filestring)
    return sorted([year] + [tup + " " + str(names_pos[tup]) for tup in names_pos])

def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
      print 'usage: [--summaryfile] file [file ...]'
      sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
      summary = True
      del args[0]

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for filename in args:
        year_name_list = extract_names(filename)
        output_string = '\n'.join(year_name_list)
        if not summary:
            print output_string
        else:
            with open(filename + ".summary", "w") as f:
                f.write(output_string)

if __name__ == '__main__':
    main()
