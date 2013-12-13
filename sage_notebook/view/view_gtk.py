"""
Windows in Gtk
"""

##############################################################################
#  Sage Notebook: A Graphical User Interface for Sage
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

import os
import sys
from gi.repository import Gtk

import sage_notebook
from sage_notebook.misc.cached_property import cached_property

from .view import ViewABC





class ViewGtk(ViewABC):

    @cached_property
    def resource_dir(self):
        return os.path.dirname(sys.modules['sage_notebook'].__file__)

    @cached_property
    def glade_file(self):
        return os.path.join(self.resource_dir, 'res', 'gtk_layout.xml')

    def make_builder(self, *object_ids):
        """
        Return the GTK builder for the specified object ids
        """
        builder = Gtk.Builder()
        builder.add_objects_from_file(self.glade_file, object_ids)
        return builder

    def terminate(self):
        Gtk.main_quit()


    ###################################################################
    # The main Notebook window

    @cached_property
    def notebook_window(self):
        from .notebook_window_gtk import NotebookWindowGtk
        notebook = NotebookWindowGtk(self.presenter, self.make_builder)
        notebook.restore_geometry(self.window_geometry.get('trac_window', {}))
        return notebook
        
