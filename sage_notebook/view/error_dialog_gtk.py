"""
Error Dialog

This is the Gtk3 implementation of :mod:`error_dialog`
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
 
from .window_gtk import ModalDialogGtk
from .error_dialog import ErrorDialogABC

class ErrorDialogGtk(ErrorDialogABC, ModalDialogGtk):

    def __init__(self, presenter, make_builder, parent, title, text):
        WINDOW = 'error_dialog'
        ErrorDialogABC.__init__(self, title, text)
        builder = make_builder(WINDOW)
        ModalDialogGtk.__init__(self, WINDOW, presenter, builder, parent)
        self.window.set_property('text', title)
        self.window.set_property('secondary_text', text)
        builder.connect_signals(self)

    def on_error_dialog_response(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
