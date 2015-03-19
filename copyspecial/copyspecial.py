#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def special(filename):
    match = re.search(r'__\w+__', filename)
    if match:
        return True
    else:
        return False

def get_special_paths(dir):
    abs_paths = []
    filenames = [fname for fname in os.listdir(dir) if special(fname)]
    for filename in filenames:
        abs_paths.append(os.path.abspath(os.path.join(dir, filename)))
    return abs_paths

def copy_to(paths, todir):
    if not os.path.exists(todir):
        os.mkdir(todir)
    for filepath in paths:
        new_path = os.path.join(todir, os.path.split(filepath)[-1])
        shutil.copy2(filepath, new_path)
    return

def zip_to(paths, tozip):
    zip_command = "zip -j %s %s" % (tozip, " ".join(paths))
    print "I'm going to execute:\n\t %s \n" % zip_command
    ret = subprocess.call(zip_command.split())
    return ret

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  for dir in args:
      special_paths = get_special_paths(dir)
      if todir:
          copy_to(special_paths, todir)
      if tozip:
          ret = zip_to(special_paths, tozip)
          return ret
      if not (todir or tozip):
          print "\n".join(special_paths)
  return 0

if __name__ == "__main__":
  main()
