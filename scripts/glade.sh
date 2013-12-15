#!/bin/sh

# Helper script to run the Glade UI designer

# rootdir=`dirname $0`

rootdir=`pwd`
echo "directory = $rootdir"
if [ ! -f "$rootdir/README.rst" ] ; then
  echo "This script must be run in the Sage Desktop project root directory"
  echo "That is, the directory containing README.rst"
fi

CATALOG_DTD=/usr/share/glade3/catalogs/glade-catalog.dtd
if [ -f "$CATALOG_DTD" ] ; then
    xmllint --dtdvalid "$CATALOG_DTD" --noout sage_notebook/view/gtk/widgets.xml
fi

export GLADE_CATALOG_SEARCH_PATH=$rootdir/sage_notebook/view/gtk
export GLADE_MODULE_SEARCH_PATH=$rootdir/sage_notebook/view/gtk

echo "GLADE_CATALOG_SEARCH_PATH=$GLADE_CATALOG_SEARCH_PATH"
echo "GLADE_MODULE_SEARCH_PATH=$GLADE_MODULE_SEARCH_PATH"

glade -v sage_notebook/res/gtk_layout.xml
