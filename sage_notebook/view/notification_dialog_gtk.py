"""
Notification Dialog

This is the Gtk3 implementation of :mod:`notification_dialog`
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
from .notification_dialog import NotificationDialogABC


class NotificationDialogGtk(NotificationDialogABC, ModalDialogGtk):

    def __init__(self, presenter, make_builder, parent, text):
        WINDOW = 'notification_dialog'
        LABEL = 'notification_label'
        NotificationDialogABC.__init__(self, text)
        builder = make_builder(WINDOW, LABEL)
        ModalDialogGtk.__init__(self, WINDOW, presenter, builder, parent_window=parent)
        label = self.label = builder.get_object(LABEL)
        label.set_text(text)
        builder.connect_signals(self)

    def on_notification_ok_clicked(self, widget, data=None):
        self.presenter.destroy_modal_dialog()

    def on_notification_dialog_close(self, widget, data=None):
        self.presenter.destroy_modal_dialog()
