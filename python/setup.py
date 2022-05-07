"""Setup the package."""
# Replace all TODO with data relevan to the current package
import glob
import os
import sys
import typing as t
from setuptools import setup


def find_package_data(base: str, globs: t.List[str], root: str) -> t.List[str]:
    """Find all interesting data files, for setup(package_data=).

    :param base: Base directory to search in.
    :type request: :class:`str`
    :param globs: A list of glob patterns to accept files.
    :type globs: List[:class:`str`]
    :param root: Directory to return paths relative to
    :type root: :class:`str`

    :return: Relevant files.
    :rtype: List[:class:`str`]
    """
    rv_dirs = [root for root, _, __ in os.walk(base)]
    relevant: t.List[str] = []
    for rv_dir in rv_dirs:
        files: t.List[str] = []
        for pat in globs:
            files += glob.glob(os.path.join(rv_dir, pat))
        if not files:
            continue
        relevant.extend([os.path.relpath(f, root) for f in files])
    return relevant


use_mypyc = os.getenv("USE_MYPYC", None) == "1"

if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    use_mypyc = True  # pylint: disable=invalid-name

if use_mypyc:
    from mypyc.build import mypycify  # pylint: disable=no-name-in-module

    MYPYC_BLACKLIST = tuple(  # TODO: fill
        os.path.join("basepath", x) for x in ("file_not_to_include")
    )

    everything = [
        os.path.join("basepath", x)
        for x in find_package_data("basepath", ["*.py"], "basepath")
    ]

    mypyc_targets = [x for x in everything if x not in MYPYC_BLACKLIST]

    mypyc_targets.sort()

    ext_modules = mypycify(
        mypyc_targets
        + [
            "--disallow-untyped-defs",
            "--disallow-incomplete-defs",
            "--strict-equality",
        ]
    )
else:
    ext_modules = []


setup(
    ext_modules=ext_modules,
)
