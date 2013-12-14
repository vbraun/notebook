"""
Command line widget
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

from gi.repository import GLib, Gdk, Gtk, Vte


class TerminalWidget(Vte.Terminal):
    __gtype_name__ = 'TerminalWidget'
    __gsignals__ = {
        #"expose_event": "override"
        'char_size_changed': 'override',
        }
 
    def __init__(self):
        Vte.Terminal.__init__(self)

    def fork_command(self, executable):
        self.set_color_background(Gdk.color_parse('white'))
        self.set_color_foreground(Gdk.color_parse('black'))
        return self.fork_command_full(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            [executable],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
        )

    def do_char_size_changed(self, width, height):
        self.set_size_request(80*width, -1)



