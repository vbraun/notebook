"""
The Notebook Window

This is the GTK3 implementation of :mod:`notebook_window`
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

import logging

from gi.repository import Gdk, Gtk, Pango
from gi.repository import GtkSource

from .window_gtk import WindowGtk
from .notebook_window import NotebookWindowABC



class NotebookWindowGtk(NotebookWindowABC, WindowGtk):

    def __init__(self, presenter, make_builder):
        WINDOW = 'notebook_window'
        builder = make_builder(WINDOW)
        WindowGtk.__init__(self, WINDOW, presenter, builder=builder)
        builder.connect_signals(self)

    def on_notebook_window_delete_event(self, widget, data=None):
        self.presenter.hide_notebook_window()
        return False

    def on_notebook_window_destroy(self, widget, data=None):
        logging.info('TODO: destroyed. autosave?')
        


    def on_notebook_menu_new_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: new")

    def on_notebook_menu_open_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: open")

    def on_notebook_menu_save_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: save")

    def on_notebook_menu_saveas_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: save as")

    def on_notebook_menu_quit_activate(self, widget, data=None):
        self.presenter.hide_notebook_window()


    def on_notebook_menu_copy_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: copy")
        
    def on_notebook_menu_paste_activate(self, widget, data=None):
        self.presenter.show_notification(self, "todo: paste")


    def on_notebook_menu_about_activate(self, widget, data=None):
        self.presenter.show_about_window()

