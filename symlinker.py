#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: Symlinker

A tool to create and modify the destination of symbolic links.

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
import sys

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "0.1"
__email__ = "dev@korvin.eu"
__status__ = "Development"


# TODO: GUI
# TODO: find all symlinks in directory
# TODO: find a specific symlink in directory
# TODO: modify symlink target
# TODO: batch modify symlinks target
# TODO: create hard link


def create_symlink(dest, sym, change=False):
    if not os.access(dest, os.F_OK):
        print("Destination doesn't exist or not accessible.")

    elif not os.access(dest, os.R_OK):
        print("You don't have permission to read destination.")

    elif change:
        if not os.access(dest, os.F_OK):
            print("Destination doesn't exist.")
        elif not os.access(dest, os.R_OK):
            print("You don't have permission to read destination.")
        elif not os.access(sym, os.F_OK):
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
        except PermissionError:
            print("You don't have permission to create symlink.")


def search_symlink(path):
    pass


def find_symlink(path, sym):
    pass


def batch_modify(path, pattern, new_pattern):
    pass


def create_hardlink(dest, sym):
    pass


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
                        default=True,
                        help="search path recursively, true by default")
    search.add_argument("-n", "--no-recursive", action="store_true",
                        help="search path non-recursively")
    # TODO: make sure -r and -n won't conflict

    # Arguments to find symlink
    find = subparsers.add_parser("find", description="Find a symbolic link.")
    find.add_argument("path", help="search this path for symbolic link")
    find.add_argument("symlink", help="search for this symbolic link")
    find.add_argument("-r", "--recursive", action="store_true",
                      default=True,
                      help="search path recursively, true by default")
    find.add_argument("-n", "--no-recursive", action="store_true",
                      help="search path non-recursively")
    # TODO: make sure -r and -n won't conflict

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
                       default=True,
                       help="modify symlinks in path and its subdirectories, "
                            "true by default")
    batch.add_argument("-n", "--no-recursive", action="store_true",
                       help="don't modify symlinks in path's subdirectories")
    # TODO: make sure -r and -n won't conflict

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

    print(args)
