#!/usr/bin/env python3
# Copyright © 2020 Aman Verma <https://aman.raoverma.com/contact.html>
# Distributed under the 0-clause BSD license, see LICENSE.md file for details.

import hashlib
import io
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
from http.client import HTTPResponse
from typing import Any, NoReturn

VERSION = "0.56.0"
# fmt: off
URL = "https://github.com/mesonbuild/meson/releases/download/{0}/meson-{0}.tar.gz".format(VERSION)
SHA256 = "291dd38ff1cd55fcfca8fc985181dd39be0d3e5826e5f0013bf867be40117213"
# fmt: on
TAR_DIR = "meson-" + VERSION


def meson_exists(expectedversion: str) -> bool:
    mesonbinary = os.path.join("meson-portable", "meson.py")

    if os.path.isfile(mesonbinary):
        # possibility of an exception here...
        mesonver: str = subprocess.run(
            [mesonbinary, "--version"],
            check=True,
            # alias for text=True that is compatible with 3.5
            universal_newlines=True,
            stdout=subprocess.PIPE,
        ).stdout.rstrip()
        return mesonver == expectedversion

    return False


def get_tar(url: str) -> bytes:
    try:
        print("Downloading {}...".format(url))
        page: HTTPResponse = urllib.request.urlopen(url)
        return page.read()
    except urllib.error.HTTPError as e:
        sys.exit("{}\nCheck if {} is up.".format(e.code, url))
    except urllib.error.URLError as e:
        sys.exit("{}\nCheck your network connection.".format(e.reason))
    finally:
        page.close()


def is_valid_hash(file: bytes, expectedhash: str) -> bool:
    return hashlib.sha256(file).hexdigest() == expectedhash


def checked_rename(src: str, dst: str) -> None:
    if src != TAR_DIR:
        sys.exit(
            "The archive extracted path was unexpected. "
            "Please try to extract it yourself"
        )
    if os.path.exists(dst):
        print("Overwriting {}.".format(dst))
        shutil.rmtree(dst)

    os.rename(src, dst)


def untar_to_dir(tar: bytes) -> None:
    with io.BytesIO(tar) as tar_io:
        with tarfile.open(fileobj=tar_io, mode="r") as tf:
            try:
                extracteddir = tf.getmembers()[0].name
                tf.extractall()
            except tarfile.CompressionError as e:
                die(e)

    checked_rename(extracteddir, "meson-portable")


def die(msg: Any) -> NoReturn:
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(1)


if not meson_exists(VERSION):
    if "-n" in sys.argv[1:]:
        sys.exit(
            "Did not find meson-{} and dry run was requested.\n".format(VERSION)
            + "Would have installed {}".format(URL)
        )
    mesontar = get_tar(URL)
    if is_valid_hash(mesontar, SHA256):
        untar_to_dir(mesontar)
        print(
            "Meson should be installed. You can run it with `./meson-portable/meson.py` on *nix"
            " and `python.exe meson-portable\\meson.py` on Windows"
        )
    else:
        sys.exit(
            "The checksum of the downloaded file does not match!\n"
            "Please download and verify the file manually."
        )
else:
    print("Found meson, skipping download.")
