#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: Symlinker

A tool to create, search and find symbolic links, or modify their
destinations.

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
__version__ = "1.1"
__email__ = "dev@korvin.eu"
__status__ = "Active"


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


def create_symlink(dest, sym, change, abs_path):
    """
    Creates or modifies a symbolic link

    :param dest: destination of symbolic link
    :type dest: str
    :param sym: name of symbolic link
    :type sym: str
    :param change: indicates whether sym has to be redirected
    :type change: bool
    :param abs_path: indicates whether the sym should convert to absolute path
    :type abs_path: bool
    """
    if abs_path:
        dest = os.path.abspath(dest)
    if not os.access(dest, os.F_OK):
        print(f"Destination doesn't exist or not accessible: '{dest}'")
    elif not os.access(dest, os.R_OK):
        print(f"You don't have permission to read destination: '{dest}'")
    elif change:
        if not os.path.islink(sym) and os.access(sym, os.F_OK):
            print(f"Target exists as a non-symlink: '{sym}'")
        elif not os.path.islink(sym):
            print(f"Symlink doesn't exist: '{sym}'")
        # with the second condition compensate for broken links
        elif not os.access(sym, os.W_OK) and not os.path.islink(sym):
            print(f"You don't have permission to modify symlink: '{sym}'")
        else:
            os.remove(sym)
            os.symlink(dest, sym)
    elif os.access(sym, os.F_OK):
        print(f"Symlink already exists: '{sym}'")
    else:
        try:
            os.symlink(dest, sym)
        except PermissionError as ex:
            print(error_message(ex))


def all_symlinks(path, recursive):
    """
    Returns a list of tuples. Each tuple contains a symbolic link and its
    destination

    :param path: path to search
    :type path: str
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    :return: list of tuples of symlinks and their destinations
    :rtype: list
    """
    if not os.access(path, os.F_OK):
        print("Path doesn't exist or not accessible.")
    elif not os.access(path, os.R_OK):
        print("You don't have permission to read path.")
    else:
        def symlinks(r):
            """
            Gathers all symlinks, first directories, then files,
            in a list of tuples

            :param r: recursive or not
            :type r: str
            :return: list of tuples of symlinks and their destinations
            :rtype: list
            """
            nonlocal path

            # These will hold the symlinks and their destinations
            file_links = []
            dir_links = []
            # Create a list of files and directories in path
            p = pathlib.Path(path).glob(r)
            # Create a case insensitive sorted list and iterate over it
            for it in sorted([str(i) for i in p],
                             key=lambda x: x.lower()):
                if os.path.islink(it):
                    # Append file links
                    if os.path.isfile(it):
                        file_links.append((it, os.readlink(it)))
                    # Append directory links
                    else:
                        dir_links.append((it, os.readlink(it)))
            # Return merged lists
            return dir_links + file_links

        if recursive:
            return symlinks("**/*")
        else:
            return symlinks("*")


def all_symlinks_generator(path, recursive):
    """
    Similar to all_symlinks() but yields results one by one

    :param path: path to search
    :type path: str
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    :return: symlink and its destination
    :rtype: tuple
    """
    if not os.access(path, os.F_OK):
        print("Path doesn't exist or not accessible.")
    elif not os.access(path, os.R_OK):
        print("You don't have permission to read path.")
    else:
        if recursive:
            r = "**/*"
        else:
            r = "*"
        p = pathlib.Path(path).glob(r)
        for i in p:
            if os.path.islink(str(i)):
                yield str(i), os.readlink(str(i))


def symlink_by_pattern(path, pattern, recursive):
    """
    Returns a list of tuples. Each tuple contains a symbolic link and its
    destination, where destination matches the given pattern

    :param path: path to search
    :type path: str
    :param pattern: pattern to search for
    :type pattern: str
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    :return: a list of tuples of symlinks and their destinations
    :rtype: list
    """
    return [i for i in all_symlinks(path, recursive) if pattern in i[1]]


def symlink_by_pattern_generator(path, pattern, recursive):
    """
    Similar to symlink_by_pattern() but yields results one by one

    :param path: path to search
    :type path: str
    :param pattern: pattern to search for
    :type pattern: str
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    :return: symlink and its destination
    :rtype: tuple
    """
    for sym, dest in all_symlinks_generator(path, recursive):
        if pattern in dest:
            yield sym, dest


def batch_modify(path, pattern, new_pattern, abs_path, recursive):
    """
    Changes the destinations of symbolic links by replacing pattern in the
    path of each destination with new_pattern

    :param path: path to search
    :type path: str
    :param pattern: pattern to search for
    :type pattern: str
    :param new_pattern: new pattern to replace pattern with
    :type new_pattern: str
    :param abs_path: indicates whether the sym should convert to absolute path
    :type abs_path: bool
    :param recursive: indicates whether to search path recursively
    :type recursive: bool
    """
    links = symlink_by_pattern(path, pattern, recursive)
    for sym, dest in links:
        # Get current working directory
        cwd = os.getcwd()
        try:
            # Change dir to directory of sym to compensate for
            # relative destination paths
            os.chdir(os.path.dirname(sym))
            # Replace path to sym with filename of sym
            sym = sym[len(os.path.dirname(sym)) + 1:]
        except FileNotFoundError:
            # sym is in cwd, can't change dir to ""
            pass
        create_symlink(dest.replace(pattern, new_pattern), sym, True, abs_path)
        # Change dir to original working directory
        os.chdir(cwd)


def create_hardlink(dest, lin):
    """
    Creates a hard link

    :param dest: existing file
    :type dest: str
    :param lin: new filename
    :type lin: str
    """
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
    linker.add_argument("-a", "--absolute_path",
                        action="store_true",
                        help="create the symlink with absolute path to its "
                             "destination")
    linker.set_defaults(which="linker")

    # Arguments to search for symlinks
    search = subparsers.add_parser("search",
                                   description="Search for symbolic links.")
    search.add_argument("path",
                        help="search this path for symbolic links")
    search.add_argument("-r", "--recursive", action="store_true",
                        help="search path recursively")
    search.add_argument("-s", "--sort", action="store_true",
                        help="sort the output. This might be a long process "
                             "and you'll see output only after it's finished")
    search.add_argument("-t", "--type", action="store_true",
                        help="type of link. Display a single character (b, "
                             "d or f) in front of each line indicating if "
                             "the link points to a broken link, directory or "
                             "a file")
    search.set_defaults(which="search")

    # Arguments to find symlink
    find = subparsers.add_parser("find",
                                 description="Find symbolic links that have "
                                             "'pattern' in their destinations")
    find.add_argument("path", help="search this path for symbolic links")
    find.add_argument("pattern",
                      help="pattern to search for in destinations")
    find.add_argument("-r", "--recursive", action="store_true",
                      help="search path recursively")
    find.add_argument("-s", "--sort", action="store_true",
                      help="sort the output. This might be a long process "
                           "and you'll see output only after it's finished")
    find.add_argument("-t", "--type", action="store_true",
                      help="type of link. Display a single character (b, d or "
                           "f) in front of each line indicating if the link "
                           "points to a broken link, directory or a file")
    find.set_defaults(which="find")

    # Arguments to batch modify symlinks
    batch = subparsers.add_parser(
        "batch",
        description="Modify all symbolic links where their destination matches"
                    " a given pattern. Redirect all of them to the "
                    "destination matching the new pattern."
    )
    batch.add_argument("path", help="search this path for symbolic links")
    batch.add_argument("pattern",
                       help="pattern to look for in the destination of "
                            "symbolic links")
    batch.add_argument("newPattern",
                       help="replace pattern with this newPattern in "
                            "symbolic links")
    batch.add_argument("-r", "--recursive", action="store_true",
                       help="search path recursively")
    batch.add_argument("-a", "--absolute_path",
                       action="store_true",
                       help="recreate the symlink with absolute path to their "
                            "destinations")
    batch.set_defaults(which="batch")

    # Arguments to search for broken symlinks
    broken = subparsers.add_parser(
        "broken",
        description="Search for broken symbolic links only"
    )
    broken.add_argument("path", help="search this path for symbolic links")
    broken.add_argument("-r", "--recursive", action="store_true",
                        help="search path recursively")
    broken.add_argument("-s", "--sort", action="store_true",
                        help="sort the output. This might be a long process "
                             "and you'll see output only after it's finished")
    broken.set_defaults(which="broken")

    # Arguments to create hard link
    hardlink = subparsers.add_parser("hardlink",
                                     description="Create a hard link.")
    hardlink.add_argument("destination",
                          help="destination where the hard link will point to")
    hardlink.add_argument("link", help="name of the hard link")
    hardlink.set_defaults(which="hardlink")

    args = parser.parse_args()

    # No arguments given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    # Create or change symlink
    if args.which == "linker":
        if args.destination is not None and args.symlink is not None:
            create_symlink(args.destination,
                           args.symlink,
                           args.change_destination,
                           args.absolute_path)

    # Batch modify symlinks
    if args.which == "batch":
        if args.path is not None \
                and args.pattern is not None \
                and args.newPattern is not None:
            print("Working. This might take a while...")
            batch_modify(args.path,
                         args.pattern,
                         args.newPattern,
                         args.absolute_path,
                         args.recursive)
            print("Done.")

    # Find symlink by pattern
    if args.which == "find":
        if args.path is not None and args.pattern is not None:
            # Choose function based on args.sort
            if args.sort:
                print("Working. This might take a long time...")
                f = symlink_by_pattern(args.path, args.pattern, args.recursive)
            else:
                f = symlink_by_pattern_generator(args.path,
                                                 args.pattern,
                                                 args.recursive)
            for symlink, destination in f:
                if args.type:
                    # Insert b, d or f at the beginning of each line
                    # for broken symlink, directory or file
                    if not os.access(symlink, os.F_OK):
                        print("b ", end="")
                    elif os.path.isdir(symlink):
                        print("d ", end="")
                    else:
                        print("f ", end="")
                print(symlink, "->", destination)

    # Search symlinks
    if args.which == "search":
        if args.path is not None:
            # Choose function based on args.sort
            if args.sort:
                print("Working. This might take a long time...")
                f = all_symlinks(args.path, args.recursive)
            else:
                f = all_symlinks_generator(args.path, args.recursive)
            for symlink, destination in f:
                if args.type:
                    # Insert b, d or f at the beginning of each line
                    # for broken symlink, directory or file
                    if not os.access(symlink, os.F_OK):
                        print("b ", end="")
                    elif os.path.isdir(symlink):
                        print("d ", end="")
                    else:
                        print("f ", end="")
                print(symlink, "->", destination)

    # Search broken symlinks
    if args.which == "broken":
        if args.path is not None:
            # Choose function based on args.sort
            if args.sort:
                print("Working. This might take a long time...")
                f = all_symlinks(args.path, args.recursive)
            else:
                f = all_symlinks_generator(args.path, args.recursive)
            for symlink, destination in f:
                if not os.access(symlink, os.F_OK):
                    print(symlink, "->", destination)

    # Create hardlink
    if args.which == "hardlink":
        if args.destination is not None and args.link is not None:
            create_hardlink(args.destination, args.link)
