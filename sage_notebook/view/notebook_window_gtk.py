"""
The Notebook Window
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

from gi.repository import Gdk, Gtk, Pango
from gi.repository import GtkSource

from .window_gtk import WindowGtk
from .notebook_window import NotebookWindowABC



class NotebookWindowGtk(NotebookWindowABC, WindowGtk):

    def __init__(self, presenter, make_builder):
        WINDOW = 'notebook_window'
        builder = make_builder(WINDOW)
        WindowGtk.__init__(self, builder, WINDOW)
        builder.connect_signals(self)
