#!/usr/bin/env bash
#
# If you have a built BCC right next to this and you ran cmake in bcc/build),
# this will set paths so you can run.

BCCBUILD=../bcc/build
PYTHONPATH=${BCCBUILD}/src/python/bcc-python3 LD_LIBRARY_PATH=${BCCBUILD}/src/cc exec python3 trip_verifier.py "$@"
