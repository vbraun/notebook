"""
Notebook Cell widget
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

from gi.repository import GLib, Gdk, Gtk, Pango
from gi.repository import GtkSource



class CellWidget(Gtk.Box):
    __gtype_name__ = 'CellWidget'


    def __init__(self, *args, **kwds):
        super().__init__(self, *args, **kwds)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        i = self._make_input()
        o = self._make_output()
        expand = False
        fill = False
        self.pack_start(i, expand, fill, 0)
        self.pack_end(o, expand, fill, 0)

    def _make_input(self):
        view = self.in_view = GtkSource.View()
        buffer = self.in_buffer = GtkSource.Buffer()
        buffer.set_text('def f(x):\n    return 1')
        view.set_buffer(buffer)
        # fontdesc = Pango.FontDescription("monospace")
        fontdesc = Pango.FontDescription("Consolas 12")
        view.modify_font(fontdesc)
        self.set_language()
        view.set_border_window_size(Gtk.TextWindowType.TOP, 15)
        view.show()
        return view

    def _make_output(self):
        view = self.out_view = Gtk.TextView()
        buffer = self.out_buffer = Gtk.TextBuffer()
        buffer.set_text('output')
        view.set_buffer(buffer)
        fontdesc = Pango.FontDescription("monospace")
        view.modify_font(fontdesc)
        view.set_border_window_size(Gtk.TextWindowType.TOP, 5)
        view.show()
        return view

    def set_language(self, language='python'):
        mgr = GtkSource.LanguageManager()
        lang = mgr.get_language(language)
        self.in_buffer.set_language(lang)
        
