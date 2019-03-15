#!/bin/sh

set -e

. venv/bin/activate
strip-hints getmeson.py > getmeson_3.5.py
$VENV_HOME/nvim/bin/black getmeson_3.5.py
