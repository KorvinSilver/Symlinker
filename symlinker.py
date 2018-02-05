#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: Symlinker

A tool to create symbolic links or modify their destinations.

Copyright 2018, Korvin F. Ezüst

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import os
import pathlib
import sys

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1"
__email__ = "dev@korvin.eu"
__status__ = "Development"


# TODO: GUI?
# TODO: find a specific symlink in directory
# TODO: batch modify symlinks target


def error_message(e):
    """
    Returns a custom error message

    :param e: error raised
    :type e: PermissionError|OSError
    :return: custom error message
    :rtype: str
    """
    errno, strerror = e.args
    return f"Error: [Errno {errno}] {strerror}"


def create_symlink(dest, sym, change):
    """
    Create or modify a symbolic link

    :param dest: destination of symbolic link
    :type dest: str
    :param sym: name of symbolic link
    :type sym: str
    :param change: indicates if sym has to be redirected
    :type change: bool
    """
    if not os.access(dest, os.F_OK):
        print("Destination doesn't exist or not accessible.")
    elif not os.access(dest, os.R_OK):
        print("You don't have permission to read destination.")
    elif change:
        if not os.access(sym, os.F_OK):
            print("Symlink doesn't exist.")
        elif not os.access(sym, os.W_OK):
            print("You don't have permission to modify symlink")
        else:
            os.remove(sym)
            os.symlink(dest, sym)
    elif os.access(sym, os.F_OK):
        print("Symlink already exists.")
    else:
        try:
            os.symlink(dest, sym)
        except PermissionError as ex:
            print(error_message(ex))


def search_symlink(path, recursive):
    """
    Searches path for symbolic links and prints them

    :param path: path to search
    :type path: str
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    """
    if not os.access(path, os.F_OK):
        print("Path doesn't exist or not accessible.")
    elif not os.access(path, os.R_OK):
        print("You don't have permission to read path.")
    else:
        def print_items(r):
            """
            Prints all symlinks, first directories, then files

            :param r: recursive or not
            :type r: str
            """
            nonlocal path
            # Create a list of files and directories in path
            p = pathlib.Path(path).glob(r)
            # Print all symlinks pointing to directories
            for item in sorted([str(i) for i in p if i.is_dir()],
                               key=lambda x: x.lower()):
                if os.path.islink(item):
                    print(os.path.abspath(item), "-->", os.readlink(item))

            # Create a list of files and directories in path
            p = pathlib.Path(path).glob(r)
            # Print all symlinks pointing to files
            for item in sorted([str(i) for i in p if i.is_file()],
                               key=lambda x: x.lower()):
                if os.path.islink(item):
                    print(os.path.abspath(item), "-->", os.readlink(item))

        if recursive:
            print_items("**/*")
        else:
            print_items("*")


def find_symlink(path, pattern):
    pass


def batch_modify(path, pattern, new_pattern):
    pass


def create_hardlink(dest, lin):
    if not os.access(dest, os.F_OK):
        print("Destination doesn't exist or not accessible.")
    elif not os.access(dest, os.R_OK):
        print("You don't have permission to read destination.")
    elif os.access(lin, os.F_OK):
        print("Target already exists.")
    else:
        try:
            os.link(dest, lin)
        except PermissionError as ex:
            print(error_message(ex))
        except OSError as ex:
            print(error_message(ex))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool to create symbolic links"
                    " or modify their destinations."
    )

    subparsers = parser.add_subparsers(help="")

    # Arguments to create or modify symlink
    linker = subparsers.add_parser("link",
                                   description="Create or modify a symbolic "
                                               "link.")
    linker.add_argument("destination",
                        help="destination where the symbolic link will "
                             "point to")
    linker.add_argument("symlink", help="name of the symbolic link")
    linker.add_argument("-c", "--change-destination",
                        action="store_true",
                        help="change the destination of the symbolic link")

    # Arguments to search for symlinks
    search = subparsers.add_parser("search",
                                   description="Search for symbolic links.")
    search.add_argument("path",
                        help="search this path for symbolic links")
    search.add_argument("-r", "--recursive", action="store_true",
                        help="search path recursively")

    # Arguments to find symlink
    find = subparsers.add_parser("find",
                                 description="Find symbolic links that have "
                                             "'pattern' in their destinations")
    find.add_argument("path", help="search this path for symbolic links")
    find.add_argument("pattern",
                      help="pattern to search for in destinations")
    find.add_argument("-r", "--recursive", action="store_true",
                      help="search path recursively")

    # Arguments to batch modify symlinks
    batch = subparsers.add_parser(
        "batch",
        description="Modify all symbolic links where their destination matches"
                    " a given pattern. Redirect all of them to the "
                    "destination matching the new pattern."
    )
    batch.add_argument("path", help="modify symbolic links in this path")
    batch.add_argument("pattern",
                       help="pattern to look for in the destination of "
                            "symbolic links")
    batch.add_argument("newPattern",
                       help="replace pattern with this newPattern in "
                            "symbolic links")
    batch.add_argument("-r", "--recursive", action="store_true",
                       help="modify symlinks in path and its subdirectories")

    # Arguments to create hard link
    hardlink = subparsers.add_parser("hardlink",
                                     description="Create a hard link.")
    hardlink.add_argument("destination",
                          help="destination where the hard link will point to")
    hardlink.add_argument("link", help="name of the hard link")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    try:
        if args.destination is not None and args.symlink is not None:
            if args.change_destination:
                create_symlink(args.destination, args.symlink, True)
            else:
                create_symlink(args.destination, args.symlink, False)
    except AttributeError:
        pass

    try:
        if args.path is not None:
            if args.recursive:
                search_symlink(args.path, True)
            else:
                search_symlink(args.path, False)
    except AttributeError:
        pass
    try:
        if args.destination is not None and args.link is not None:
            create_hardlink(args.destination, args.link)
    except AttributeError:
        pass
