#!/usr/bin/env python3
# Download meson to the current directory.
#
# Copyright 2019 Aman Verma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import io
import os
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
from typing import Any

VERSION = "0.49.0"
# fmt: off
URL = "https://github.com/mesonbuild/meson/releases/download/{0}/meson-{0}.tar.gz".format(VERSION)
SHA512 = "f36994d1a030c985a51aa335eaceea608dcb1692cea7d2d4caeeb2b3bf471837dffdc502aa940742eb8c605d15b8adb35ba36b7da5d10455b7fd0ef5a48663e3"
# fmt: on
TAR_DIR = "meson-" + VERSION


def eprintf(fmtstring: str, *args: Any) -> None:
    print(fmtstring.format(*args), file=sys.stderr)


def exists(expectedversion: str) -> bool:
    mesonbinary = os.path.join("meson", "meson.py")
    if os.path.isfile(mesonbinary):
        # could throw exception, but it probably won't
        mesonver: str = subprocess.run(
            [mesonbinary, "--version"],
            check=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
        ).stdout.rstrip()
        return mesonver == expectedversion
    return False


def gettar(url: str) -> bytes:
    try:
        print("Downloading {}...".format(url))
        return urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        eprintf(str(e.code))
        sys.exit(1)
    except urllib.error.URLError as e:
        eprintf("{}\nCheck your network connection.", e.reason)
        sys.exit(1)


def isvalidhash(file: bytes, expectedhash: str) -> bool:
    hasher = hashlib.sha512(file)
    return hasher.hexdigest() == expectedhash


def checkedrename(src: str, dst: str) -> None:
    if src != TAR_DIR:
        eprintf(
            "The archive extracted path was unexpected. "
            "Please try to extract it yourself"
        )
        sys.exit(1)
    if os.path.exists(dst):
        eprintf("Renaming {0} to {1} would overwrite. Please remove {1}.", src, dst)
        sys.exit(1)

    os.rename(src, dst)


def untar(tar: io.BytesIO) -> None:
    try:
        t = tarfile.open(fileobj=tar, mode="r")
        ogdir: str = t.getmembers()[0].name
        t.extractall()
    except tarfile.CompressionError as e:
        print(str(e), file=sys.stderr)
    else:
        checkedrename(ogdir, "meson")
    finally:
        # not ideal to close in function.
        tar.close()
        t.close()


if not exists(VERSION):
    if "-n" in sys.argv[1:]:
        eprintf(
            "Did not find meson-{} and dry run was requested.\nWould have installed {}",
            VERSION,
            URL,
        )
        sys.exit(1)
    mesontar = gettar(URL)
    if isvalidhash(mesontar, SHA512):
        untar(io.BytesIO(mesontar))
        print(
            "Meson should be installed. You can run it with `meson/meson.py` on *nix",
            "and `python.exe meson\\meson.py` on Windows",
        )
    else:
        eprintf(
            "The checksum of the downloaded file does not match!\n"
            "Please download and verify the file manually."
        )
else:
    print("Found meson, skipping download.")
    sys.exit(0)
