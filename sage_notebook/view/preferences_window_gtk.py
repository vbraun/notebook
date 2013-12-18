"""
Preferences Window

This is the GTK3 implementation of :mod:`preferences_window`
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
 
from .preferences_window import PreferencesWindowABC
from .window_gtk import WindowGtk


class PreferencesWindowGtk(PreferencesWindowABC, WindowGtk):

    def __init__(self, presenter, make_builder):
        WINDOW = 'preferences_window'
        builder = make_builder(WINDOW)
        WindowGtk.__init__(self, WINDOW, presenter, builder=builder)
        builder.connect_signals(self)

    def on_prefs_window_response(self, widget, data=None):
        self.presenter.hide_about_window()

