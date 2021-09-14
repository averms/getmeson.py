getmeson.py
===========

description
-----------
A Python script that downloads a release of the Meson build system to
`./meson-portable/`. Use it in your projects if your `meson.build` uses new
Meson features not widely available in Linux distro repositories yet and you
don't want to require users to `pip install meson`. Also use it to freeze a
specific version of Meson that you know works correctly.

usage
-----
Copy the the file `getmeson.py` into your source tree. Update `VERSION`,
`URL`, and `SHA256` at the top of the script when you want to change the
version it downloads.

options
-------
`-n` signals a dry run (print what is going to be downloaded).

exit status
-----------
Exit code of 0 is good, it means you already have Meson or the download was
successful. Exit code of 1 means that something went wrong.

license
-------
Distributed under the 0-clause BSD license, a [public-domain-equivalent
license](https://en.wikipedia.org/wiki/Public-domain-equivalent_license)
approved by the Open Source Initiative.
