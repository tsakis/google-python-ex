#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib  # for urlretrieve, somewhat faster
import urllib2 # for urlopen
import subprocess

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  try:
      hostname = filename.split("_")[1]
  except IndexError, e:
      print "No '_' found in filename %s: Check log filename!" % (filename)
      sys.exit(1)
  with open(filename, "r") as f:
      log_string = f.read()
  urls = set(re.findall(r"GET\s([a-zA-Z0-9-/.]+.jpg)\sHTTP", log_string))
  sorted_urls = sorted(urls, key = lambda x : x.split("/")[-1].split(".")[0].split("-")[-1])
  return ["http://" + hostname + url for url in sorted_urls]

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
      os.mkdir(dest_dir)
  for i, url in enumerate(img_urls):
      print "Retrieving image file %d" % (i + 1)
      urllib.urlretrieve(url, dest_dir + "/img" + str(i))
      """
      try:
          http_obj = urllib2.urlopen(url)
      except urllib2.URLError, e:
          print "Could not get %s: %s" % (url, e)
          continue
      with open(dest_dir + "/img" + str(i), "wb") as f:
          f.write(http_obj.read())
      """
  with open(dest_dir + "/index.html", "w") as f:
      f.write("<verbatim>\n<html>\n<body>")
      for i in range(len(img_urls)):
          f.write('<img src="img%s">' %i)
      f.write("</body></html>")
  return

def open_image(dest_dir):
    subprocess.call(["google-chrome", dest_dir + "/index.html"])
    return

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  if todir:
    download_images(img_urls, todir)
    open_image(todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
