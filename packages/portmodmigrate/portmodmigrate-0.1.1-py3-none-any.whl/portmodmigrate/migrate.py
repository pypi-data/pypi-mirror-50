# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Any
import os
import sys
import argparse
from queue import PriorityQueue
from functools import lru_cache, total_ordering
from fuzzywuzzy import fuzz
from portmod.repo.loader import load_all
from portmod.repo.util import get_hash
from portmod.repo.download import get_filename
from portmod.globals import env
from portmod.log import warn
from portmod.colour import green
from portmod.prompt import prompt_bool, prompt_num
from portmod.query import display_search_results
from portmod.main import configure_mods
from portmod.configfile import find_config, read_config, remove_config, write_config
from portmod.config import get_config
from portmod.repo.manifest import SHA512
from .datadir import find_esp_bsa


@total_ordering
class PrioritizedItem:
    priority: int
    item: Any

    def __init__(self, priority, item):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority


def migrate():
    parser = argparse.ArgumentParser(
        description="Command line tool for migrating mod setup to portmod"
    )
    parser.add_argument(
        "--import-archives",
        metavar="DIR",
        help="Imports archives from the given directory. If directory is not specified,"
        "looks for them in both the current directory and the cache directory",
        nargs="?",
    )
    parser.add_argument(
        "--scan-installed-mods",
        help="Scans mods in openmw.cfg and creates a list of mods in the repository "
        "that would satisfy as many mods as possible. If run with the interactive "
        "option, prompts to handle ambiguous mods and also prompts to install them",
        action="store_true",
    )
    parser.add_argument(
        "--pretend",
        help="Instead of committing changes, just show what would have been done "
        "(only affects --import-archives)",
        action="store_true",
    )
    parser.add_argument(
        "--interactive", help="Resolve ambiguity interactively", action="store_true"
    )
    parser.add_argument(
        "--fuzzy",
        help="Does fuzzy matching when scanning mods (experimental)",
        action="store_true",
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.import_archives is not None:
        # Create mapping of hashes to file names
        sources = list(
            [
                source
                for mod in load_all()
                for source in mod.get_sources([], [], matchall=True)
            ]
        )
        hashes = {}
        for source in sources:
            for h in source.hashes:
                if h.alg == SHA512:
                    hashes[h.value] = source.name

        # Hash each file in the given directory. If it is in our map, rename it
        root = args.import_archives
        files = os.listdir(root)
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                shasum = get_hash(path)
                if shasum in hashes:
                    dest = get_filename(hashes[shasum])
                    if not os.path.exists(dest):
                        print("Moving {} -> {}".format(path, dest))
                        if not args.pretend:
                            os.rename(path, dest)
                    else:
                        print("Skipping {}. Already in cache".format(path))
        if args.pretend:
            warn(
                "The above changes have not actually been applied. "
                "To apply these changes, rerun the command without the --pretend flag"
            )

    if args.scan_installed_mods:
        config = read_config(os.path.expanduser(get_config()["OPENMW_CONFIG"]))
        mods = []
        ambiguousmods = []
        fuzzymods = []
        ambiguousfuzzymods = []

        # Try to find possible replacement mods in the repo
        for index, path in find_config(config, "data=*"):
            path = path.replace("data=", "")
            fullpath = (
                os.path.normpath(os.path.expanduser(path)).lstrip('"').rstrip('"')
            )
            if not fullpath.startswith(env.MOD_DIR):
                modq = find_mod(fullpath)
                if isinstance(modq, PriorityQueue):
                    if modq.qsize() == 1:
                        mods.append((path, modq.get().item))
                    elif modq.qsize() > 1:
                        if args.interactive:
                            result = prompt_mods(path, modq)
                            if result is not None:
                                mods.append(result)
                        else:
                            ambiguousmods.append((path, modq.get().item))
                    elif args.fuzzy:
                        fuzzymodq = find_fuzzy_mod(fullpath)
                        if fuzzymodq.qsize() > 1:
                            if args.interactive:
                                result = prompt_mods(path, fuzzymodq)
                                if result is not None:
                                    fuzzymods.append(result)
                            elif fuzzymodq.qsize() == 1:
                                fuzzymods.append((path, fuzzymodq.get().item))
                            else:
                                ambiguousfuzzymods.append((path, fuzzymodq.get().item))
                        else:
                            warn("Could not find mod in repo for {}".format(path))
                    else:
                        warn("Could not find mod in repo for {}".format(path))
                else:  # Is a pybuild that perfectly matched the directory
                    mods.append((path, modq))

        # Present changes to user and prompt them to apply them automatically
        # Also print command in case they want to install the mods manually
        modnames = []
        paths = []

        print()

        if mods:
            print(
                "The following mods matched unambiguously "
                "using plugin and archive file names:"
            )

            for (path, mod) in mods:
                print("{} : {}".format(green(mod.ATOM), path))
                modnames.append(mod.ATOM.CMN)
                paths.append(path)

        if ambiguousmods:
            warn(
                "The following mods matched ambiguously using plugin and archive "
                "file names. Double check this list before continuing, or rerun with "
                "--interactive if you would like to check the other possible matches"
            )
            for (path, mod) in ambiguousmods:
                print("{} : {}".format(green(mod.ATOM), path))
                modnames.append(mod.ATOM.CMN)
                paths.append(path)

        if fuzzymods:
            warn(
                "The following mods matched unambiguously using fuzzy search on their "
                "directory name. Double check these before continuing."
            )
            for (path, mod) in fuzzymods:
                print("{} : {}".format(green(mod.ATOM), path))
                modnames.append(mod.ATOM.CMN)
                paths.append(path)

        if ambiguousfuzzymods:
            warn(
                "The following mods matched ambiguously using fuzzy search on their "
                "directory name. Double check this list before continuing, or rerun "
                "with --interactive if you would like to check the other possible "
                "matches"
            )
            for (path, mod) in ambiguousfuzzymods:
                print("{} : {}".format(green(mod.ATOM), path))
                modnames.append(mod.ATOM.CMN)
                paths.append(path)

        command = "omwmerge "
        command += " ".join(modnames)

        if not modnames:
            print("Nothing to do.")
            return

        # If interactive, prompt to install mods,
        # removing outdated lines from the config
        if args.interactive:
            if prompt_bool(
                "Would you like to replace the above manually installed mods "
                "with the ones in the repository?"
            ):

                config = read_config(os.path.expanduser(get_config()["OPENMW_CONFIG"]))
                for path in paths:
                    remove_config(config, f"data=*{path}*")

                write_config(get_config()["OPENMW_CONFIG"], config)
                configure_mods(modnames, update=True, newuse=True, noreplace=True)
        else:
            print('To install these mods, run "{}"'.format(command))


def prompt_mods(path, modq):
    """
    Prompts the user to select from a list of mods that may match
    the mod installed at the given path
    """
    desc = (
        "The above mods partially matched the mod "
        "installed at {}. Higher priority means closer match.\n"
        "Which would you like to select? 0 - {}, "
        "or -1 to select none".format(path, modq.qsize() - 1)
    )

    modlist = []
    while not modq.empty():
        modlist.append(modq.get())

    i = 0
    for pitem in modlist:
        print("{}) Priority: {}".format(i, 100 - pitem.priority))
        display_search_results([pitem.item], summarize=False)
        i += 1

    index = prompt_num(desc, len(modlist), cancel=True)
    if index == -1:
        return None
    return (path, modlist[index].item)


@lru_cache(maxsize=None)
def get_plugin_map():
    m = {}
    for mod in load_all():
        m[
            frozenset(
                [file.NAME for idir in mod.INSTALL_DIRS for file in idir.get_files()]
            )
        ] = mod
    print(m)
    return m


def find_mod(path):
    """
    Determines possible mods installed at the given path
    using the contained plugin files
    """
    # Collect esps and bsas in directory (recursively)
    files = set()
    for root, _, _ in os.walk(path):
        esps, bsas = find_esp_bsa(root)
        files |= set(esps)
        files |= set(bsas)

    files = frozenset(files)

    if not files:
        return PriorityQueue()

    # Find mods matching the given files
    # If we only find a perfect match, return immediately. This is f
    m = get_plugin_map()
    if m.get(files) is not None:
        return m[files]

    modq = PriorityQueue()
    for key in m:
        length = len(files.intersection(key))
        if length > 0:
            modq.put(PrioritizedItem(len(files) - length, m[key]))
    return modq


def find_fuzzy_mod(path):
    """
    Determines possible mods installed at the given path using fuzzy search
    on the directory name
    """
    name = os.path.basename(path).rstrip('"')
    modq = PriorityQueue()
    seen = set()
    for mod in load_all():
        match = fuzz.token_set_ratio(name, mod.NAME)
        # PriorityQueues work on lowest items, so reverse the value
        if mod.ATOM.CM not in seen:
            modq.put(PrioritizedItem(100 - match, mod))
            seen.add(mod.ATOM.CM)

    # If any matches are greater than 90%, return them
    results = PriorityQueue()
    nextentry = modq.get()

    while nextentry.priority <= 10 and not modq.empty():
        results.put(nextentry)
        nextentry = modq.get()

    if modq.empty() and nextentry.priority <= 10:
        results.put(nextentry)

    # Otherwise, return best 5 that are greater than 50%
    # to avoid overwhelming user with weak matches
    threshold = 50
    if results.empty():
        i = 5
        if nextentry.priority <= threshold:
            results.put(nextentry)
            nextentry = modq.get()
            i -= 1

        while i > 0 and nextentry.priority <= threshold and not modq.empty():
            results.put(nextentry)
            nextentry = modq.get()
            i -= 1

        if i > 0 and nextentry.priority <= threshold and modq.empty():
            results.put(nextentry)

    return results
