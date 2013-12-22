#!/bin/sh

# Helper script for virtual install flask socket

rootdir=`pwd`
echo "directory = $rootdir"
if [ ! -f "$rootdir/README.rst" ] ; then
  echo "This script must be run in the Sage Desktop project root directory"
  echo "That is, the directory containing README.rst"
fi

set -e

virtualenv bin

./bin/bin/pip install Flask-Sockets
