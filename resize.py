#!/usr/bin/env python

"""
Quick and dirty resize of @2x files contained in an .xcassets asset catalog

Uses ImageMagick resize command - could in future use a Python image module
"""

import os
import json
import argparse
import commands

__author__ = 'Matthew Kennard'
__copyright__ = "Copyright 2013, One Result Ltd"
__license__ = "MIT"
__version__ = "0.0.1"


def escape_filename(filename):
    """
    Escape the filename suitable for including in a command line call

    @param filename
    @return escaped filename
    """
    return filename.replace(' ', '\\ ')


def resize_image(in_file, out_file):
    """
    For quickness of implementation use ImageMagick

    @param in_file: @2x file
    @param out_file: @1x file to write

    @return: True if resize was successful
    """
    print 'Resizing: convert %s -resize 50%% %s' % (escape_filename(in_file), escape_filename(out_file))
    s, o = commands.getstatusoutput('convert %s -resize 50%% %s' % (escape_filename(in_file), escape_filename(out_file)))
    if s == 0:
        return True
    return False


def paths_of_contents_json(xcassets_path):
    """
    @return: paths relative to xcassets_path of all Contents.json files
    """
    paths = []
    for path in os.walk(xcassets_path):
        if 'Contents.json' in path[2]:
            paths.append(path[0])
    return paths


def resize_icons_in_contents_json(directory):
    """
    Resize all of the @2x images to @1x in a directory containing a Contents.json file

    @param directory: directory containing a Contents.json file and images
    """
    json_path = os.path.join(directory, 'Contents.json')
    dictionary = json.loads(open(json_path).read())
    if 'images' not in dictionary:
        print 'No images key'
        return
    if len(dictionary['images']) != 2:
        print 'Unexpected number of images'
        return
    image_2x = dictionary['images'][1]
    image_2x_path = os.path.join(directory, image_2x['filename'])
    image_1x_path = image_2x_path.replace('@2x', '')
    if resize_image(image_2x_path, image_1x_path):
        dictionary['images'][0]['filename'] = os.path.basename(image_1x_path)
        json_out = open(json_path, 'w')
        json.dump(dictionary, json_out)
        json_out.close()


def resize_all(xcassets_path):
    """
    Perform a resize on all @2x images referenced in xcassets_path
    """
    directories = paths_of_contents_json(xcassets_path)
    for directory in directories:
        resize_icons_in_contents_json(directory)


def main():
    parser = argparse.ArgumentParser(description='Resize @2x images in .xcassets.')
    parser.add_argument('xcassets', metavar='XCASSETS', type=str, nargs=1, help='relative path to .xcassets')
    args = parser.parse_args()
    resize_all(args.xcassets[0])


if __name__ == '__main__':
    main()