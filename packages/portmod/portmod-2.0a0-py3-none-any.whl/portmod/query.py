# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for performing bulk queries on the mod database and repositories
"""

from typing import Dict, Iterable, List, Set, Tuple
import argparse
import re
import sys
import traceback
from .globals import env
from .colour import green, blue, bright, lblue, red, yellow
from .log import err
from .config import get_config
from .pybuild_interface import Pybuild
from .repo.manifest import get_total_download_size
from .repo.loader import load_all, load_all_installed, load_installed_mod
from .repo.util import get_newest_mod
from .repo.atom import Atom, atom_sat
from .repo.use import use_reduce
from .repo.metadata import get_mod_metadata


def compose(*functions):
    """
    Composes the given single-argument functions
    """

    def inner(arg):
        for func in reversed(functions):
            arg = func(arg)
        return arg

    return inner


def str_strip(value: str) -> str:
    return re.sub("(( +- +)|(:))", "", value)


def str_squelch_sep(value: str) -> str:
    return re.sub("(-|_|/)", " ", value)


def query(
    field, value, strip=False, squelch_sep=False, insensitive=False, installed=False
) -> Set[Pybuild]:
    """
    Finds mods that contain the given value in the given field
    """

    def func(val: str) -> str:
        result = val
        if insensitive:
            result = result.lower()
        if strip:
            result = str_strip(result)
        if squelch_sep:
            result = str_squelch_sep(result)
        return result

    search = func(value)

    if installed:
        mods = [mod for group in load_all_installed().values() for mod in group]
    else:
        mods = load_all()

    return {mod for mod in mods if search in func(getattr(mod, field))}


def query_depends(atom: Atom, all_mods=False) -> List[Tuple[Atom, str]]:
    """
    Finds mods that depend on the given atom
    """
    if all_mods:
        mods = load_all()
    else:
        mods = [mod for group in load_all_installed().values() for mod in group]

    depends = []
    for mod in mods:
        if not all_mods:
            enabled, disabled = mod.get_use()
            atoms = use_reduce(
                mod.RDEPEND, enabled, disabled, token_class=Atom, flat=True
            )
        else:
            atoms = use_reduce(mod.RDEPEND, token_class=Atom, matchall=True, flat=True)

        for dep_atom in atoms:
            if dep_atom != "||" and atom_sat(dep_atom, atom):
                depends.append((mod.ATOM, dep_atom))
    return depends


def display_search_results(
    mods: Iterable[Pybuild], summarize: bool = True, file=sys.stdout
):
    """
    Prettily formats a list of mods for use in search results
    """
    groupedmods: Dict[str, List[Pybuild]] = {}
    for mod in mods:
        if groupedmods.get(mod.CMN) is None:
            groupedmods[mod.CMN] = [mod]
        else:
            groupedmods[mod.CMN].append(mod)

    sortedgroups = sorted(groupedmods.values(), key=lambda group: group[0].NAME)

    for group in sortedgroups:
        sortedmods = sorted(group, key=lambda mod: mod.MV)
        newest = get_newest_mod(group)
        installed = load_installed_mod(Atom(newest.CMN))
        download = get_total_download_size([newest])

        if installed is not None:
            installed_str = blue(bright(installed.MV))

            enabled = installed.INSTALLED_USE & installed.IUSE_EFFECTIVE
            disabled = installed.IUSE_EFFECTIVE - enabled
            texture = next(
                (
                    use
                    for use in installed.INSTALLED_USE
                    if use.startswith("texture_size_")
                ),
                None,
            )
            enabled.discard(texture)
            disabled = set(
                filter(lambda x: not x.startswith("texture_size_"), disabled)
            )

            if enabled or disabled or texture:
                installed_str += " {" + "{}".format(
                    " ".join(
                        sorted(map(compose(bright, red), enabled))
                        + sorted(map(blue, disabled))
                    )
                )
                if texture:
                    if enabled or disabled:
                        installed_str += " "
                    installed_str += "TEXTURE_SIZE" + '="{}"'.format(
                        bright(red(texture.lstrip("texture_size_")))
                    )
                installed_str += "}"
        else:
            installed_str = "not installed"

        # List of version numbers, prefixed by either (~) or ** depending on
        # keyword for user's arch. Followed by use flags, including use expand
        version_str = ""
        versions = []
        ARCH = get_config()["ARCH"]
        for mod in sortedmods:
            if ARCH in mod.KEYWORDS:
                versions.append(green(mod.MV))
            elif "~" + ARCH in mod.KEYWORDS:
                versions.append(yellow("(~)" + mod.MV))
            else:
                versions.append(red("**" + mod.MV))
        version_str = " ".join(versions)
        flags = sorted({flag for mod in group for flag in mod.IUSE})
        textures = mod.TEXTURE_SIZES
        if flags or textures:
            version_str += " {" + "{}".format(lblue(" ".join(flags)))
            if textures:
                if flags:
                    version_str += " "
                version_str += "TEXTURE_SIZES" + '="{}"'.format(
                    lblue(" ".join(textures.split()))
                )
            version_str += "}"

        # If there are multiple URLs, remove any formatting from the pybuild and
        # add padding
        homepage_str = "\n                 ".join(newest.HOMEPAGE.split())
        mod_metadata = get_mod_metadata(mod)

        print(
            "{}  {}".format(green("*"), bright(newest.CMN)),
            "       {} {}".format(green("Name:"), mod.NAME),
            "       {} {}".format(green("Available Versions: "), version_str),
            "       {} {}".format(green("Installed version:  "), installed_str),
            "       {} {}".format(green("Size of files:"), download),
            "       {} {}".format(green("Homepage:"), homepage_str),
            "       {} {}".format(green("Description:"), newest.DESC),
            "       {} {}".format(green("License:"), newest.LICENSE),
            sep="\n",
            file=file,
        )

        if mod_metadata and mod_metadata.get("upstream"):
            maintainer = mod_metadata["upstream"].get("maintainer")
            if maintainer:
                print(
                    "       {} {}".format(
                        green("Upstream Author/Maintainer:"),
                        maintainer.name or maintainer.email,
                    ),
                    file=file,
                )

        print(file=file)

    if summarize:
        print("\nMods found: {}".format(len(sortedgroups)), file=file)


def query_main():
    """
    Main function for omwquery executable
    """
    parser = argparse.ArgumentParser(
        description="Command line interface to query information about portmod mods"
    )
    parser.add_argument("--debug", help="Enables debug traces", action="store_true")
    subparsers = parser.add_subparsers()
    depends = subparsers.add_parser(
        "depends", help="list all mods directly depending on ATOM"
    )
    depends.add_argument("ATOM")
    depends.add_argument(
        "-a",
        "--all",
        help="Also query mods that are not installed",
        action="store_true",
    )

    def depends_func(args):
        print(" * These mods depend on {}:".format(bright(args.ATOM)))
        for mod_atom, dep_atom in query_depends(Atom(args.ATOM), args.all):
            print("{} ({})".format(green(mod_atom), dep_atom))

    depends.set_defaults(func=depends_func)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.debug:
        env.DEBUG = True
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            traceback.print_exc()
            err("{}".format(e))
            exit(1)
