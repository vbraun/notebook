"""
Setup Assistant Dialog

This is the Gtk3 implementation of :mod:`setup_assistant_dialog`
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
logger = logging.getLogger('GUI')
 
from .window_gtk import ModalDialogGtk
from .setup_assistant_dialog import SetupAssistantDialogABC



class SetupAssistantDialogGtk(SetupAssistantDialogABC, ModalDialogGtk):

    def __init__(self, presenter, make_builder, parent, sage_root, callback):
        WINDOW = 'setup_assistant'
        SAGE_ROOT = 'setup_sage_root'
        CONFIRM = 'setup_confirmation'
        CONTENT = 'setup_content'
        SetupAssistantDialogABC.__init__(self, sage_root, callback)
        builder = make_builder(WINDOW, SAGE_ROOT, CONFIRM, CONTENT)
        ModalDialogGtk.__init__(self, WINDOW, presenter, builder, parent_window=parent)
        self.sage_root_entry = builder.get_object(SAGE_ROOT)
        self.content = builder.get_object(CONTENT)
        if sage_root is None:
            sage = self.presenter.get_sage_installation(None)
            if sage.is_usable:
                sage_root = sage.sage_root
        if sage_root is not None:
            self.sage_root_entry.set_text(sage_root)
        self.confirmation = builder.get_object('setup_confirmation')
        builder.connect_signals(self)

    def on_setup_assistant_apply(self, widget, data=None):
        logger.debug('setup assistant apply (%s)', data)
        self.callback(self.sage)

    def on_setup_assistant_close(self, widget, data=None):
        logger.debug('setup assistant close (%s)', data)
        self.presenter.destroy_modal_dialog()

    def on_setup_assistant_cancel(self, widget, data=None):
        logger.debug('setup assistant cancel (%s)', data)
        self.presenter.destroy_modal_dialog()

    def on_setup_assistant_prepare(self, widget, data=None):
        if data is self.content:
            self.sage_root_entry.select_region(0, -1)
        if data is self.confirmation:
            self.sage_root = path = self.sage_root_entry.get_text()
            self.sage = self.presenter.get_sage_installation(path)
            s = '<i>Directory:</i>\n'
            s += '   ' + path + '\n\n'
            if self.sage.is_usable:
                s += '<i>Version:</i>\n'
                s += '   ' + self.sage.version + '\n\n'
                s += '<b>Found Sage installation</b>\n'
                if self.sage.has_git:
                    s += '<b>Uses Git</b>\n'
                else:
                    s += '<b>Too old to use Git</b>\n'
            else:
                s += '<b>Error: no usable Sage installation</b>\n'
            self.confirmation.set_markup(s)
            self.window.set_page_complete(self.confirmation, self.sage.is_usable)


    

