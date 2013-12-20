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
        super().terminate()
        Gtk.main_quit()


    ###################################################################
    # The about window

    @cached_property
    def about_window(self):
        from .about_window_gtk import AboutWindowGtk
        about = AboutWindowGtk(self.presenter, self.make_builder)
        return about


    ###################################################################
    # The main Notebook window

    @cached_property
    def notebook_window(self):
        from .notebook_window_gtk import NotebookWindowGtk
        notebook = NotebookWindowGtk(self.presenter, self.make_builder)
        geometry = self.presenter.get_saved_geometry(notebook.name())
        notebook.restore_geometry(geometry)
        return notebook
        

    ###################################################################
    # The preferences dialog

    @cached_property
    def preferences_dialog(self):
        from .preferences_dialog_gtk import PreferencesDialogGtk
        prefs = PreferencesDialogGtk(self.presenter, self.make_builder)
        return prefs

    def populate_preferences_dialog(self, config):
        self.preferences_dialog.apply(config)

    ###################################################################
    # Modal dialogs

    def new_notification_dialog(self, parent, text):
        from .notification_dialog_gtk import NotificationDialogGtk
        dlg = NotificationDialogGtk(self.presenter, self.make_builder, parent, text)
        assert self._current_dialog is None
        self._current_dialog = dlg
        return dlg

    def new_error_dialog(self, parent, title, text):
        from .error_dialog_gtk import ErrorDialogGtk
        dlg = ErrorDialogGtk(self.presenter, self.make_builder, parent, title, text)
        assert self._current_dialog is None
        self._current_dialog = dlg
        return dlg
        
    def new_setup_assistant(self, parent, sage_root, callback):
        from .setup_assistant_dialog_gtk import SetupAssistantDialogGtk
        dlg = SetupAssistantDialogGtk(self.presenter, self.make_builder, parent, 
                                      sage_root, callback)
        assert self._current_dialog is None
        self._current_dialog = dlg
        return dlg
        
