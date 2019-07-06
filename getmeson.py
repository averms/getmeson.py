#!/usr/bin/env python3
# Download meson to the current directory.
#
# Copyright 2019 Aman Verma
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
import subprocess
import sys

VERSION = "0.51.0"
# fmt: off
URL = "https://github.com/mesonbuild/meson/releases/download/{0}/meson-{0}.tar.gz".format(VERSION)
SHA256 = "2f75fdf6d586d3595c03a07afcd0eaae11f68dd33fea5906a434d22a409ed63f"
# fmt: on
TAR_DIR = "meson-" + VERSION


def exists(expectedversion: str) -> bool:
    mesonbinary = os.path.join("meson", "meson.py")

    if os.path.isfile(mesonbinary):
        # possibility of an exception here...
        mesonver: str = subprocess.run(
            [mesonbinary, "--version"],
            check=True,
            # alias for text that is compatible with 3.5
            universal_newlines=True,
            stdout=subprocess.PIPE,
        ).stdout.rstrip()
        return mesonver == expectedversion

    return False


def gettar(url: str) -> bytes:
    import urllib.error
    import urllib.request

    try:
        print("Downloading {}...".format(url))
        page = urllib.request.urlopen(url)
        return page.read()
    except urllib.error.HTTPError as e:
        sys.exit("{}\nCheck if {} is up.".format(e.code, url))
    except urllib.error.URLError as e:
        sys.exit("{}\nCheck your network connection.".format(e.reason))
    finally:
        page.close()


def isvalidhash(file: bytes, expectedhash: str) -> bool:
    import hashlib

    return hashlib.sha256(file).hexdigest() == expectedhash


def checkedrename(src: str, dst: str) -> None:
    if src != TAR_DIR:
        sys.exit(
            "The archive extracted path was unexpected. "
            "Please try to extract it yourself"
        )
    if os.path.exists(dst):
        import shutil

        print("Overwriting {}.".format(dst))
        shutil.rmtree(dst)

    os.rename(src, dst)


def untartodir(tar: bytes) -> None:
    import tarfile

    try:
        tarbuffered: io.BytesIO = io.BytesIO(tar)
        t = tarfile.open(fileobj=tarbuffered, mode="r")
        extracteddir = t.getmembers()[0].name
        t.extractall()
    except tarfile.CompressionError as e:
        print(str(e), file=sys.stderr)
    else:
        checkedrename(extracteddir, "meson")
    finally:
        tarbuffered.close()
        t.close()


if not exists(VERSION):
    if "-n" in sys.argv[1:]:
        sys.exit(
            (
                "Did not find meson-{} and dry run was requested.\n"
                "Would have installed {}"
            ).format(VERSION, URL)
        )
    mesontar = gettar(URL)
    if isvalidhash(mesontar, SHA256):
        untartodir(mesontar)
        print(
            "Meson should be installed. You can run it with `./meson/meson.py` on *nix"
            " and `python.exe meson\\meson.py` on Windows"
        )
    else:
        sys.exit(
            "The checksum of the downloaded file does not match!\n"
            "Please download and verify the file manually."
        )
else:
    print("Found meson, skipping download.")
