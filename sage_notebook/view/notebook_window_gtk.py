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

from .window_gtk import WindowGtk
from .notebook_window import NotebookWindowABC
from .gtk.cell_widget import (
    CellVerticalSpacerWidget, CellWidget
)

# background-color: rgba (0,0,0,1); 

WINDOW = 'notebook_window'
TITLE = 'notebook_title'
DESCRIPTION_VIEW = 'notebook_description_view'
DESCRIPTION_MODEL = 'notebook_description_model'
CELLS = 'notebook_cells_box'

NOTEBOOK_STYLE_CSS = """
#{title} {{
    border-radius: 0;
    border-style: solid;
    border-width: 0;
    font-size: 400%;
}}

#{title}:focused {{
}}

#{description} {{
    font-size: 50%;
}}

#{cells} *  {{
    color: black;
    background: white;
}}

#{cells} CellLabelWidget {{
    color: grey;
    font-size: 90%;
}}


""".format(
    window=WINDOW, 
    title=TITLE, 
    description=DESCRIPTION_VIEW,
    cells=CELLS
).encode('utf-8')





class NotebookWindowGtk(NotebookWindowABC, WindowGtk):

    def __init__(self, presenter, make_builder):
        builder = make_builder(WINDOW, TITLE, DESCRIPTION_VIEW, DESCRIPTION_MODEL, CELLS)
        WindowGtk.__init__(self, WINDOW, presenter, builder=builder)
        self._init_title(builder.get_object(TITLE))
        self._init_description(builder.get_object(DESCRIPTION_VIEW),
                               builder.get_object(DESCRIPTION_MODEL))
        self._init_cells(builder.get_object(CELLS))

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(NOTEBOOK_STYLE_CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), 
            style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        builder.connect_signals(self)

    def _init_title(self, title):
        self.title = title
        title.set_name(TITLE)
        #font_description = Pango.FontDescription('Lucida Sans 48')
        #title.modify_font(font_description)

    def _init_description(self, view, model):        
        self.desc_view = view
        self.desc_model = model
        font_description = Pango.FontDescription('Lucida Sans 10')
        view.modify_font(font_description)
        view.set_border_window_size(Gtk.TextWindowType.BOTTOM, 10)


    def _init_cells(self, cells):
        self.cells = cells
        cells.set_name(CELLS)
        expand = False
        fill = True
        c1, c2, c3 = CellWidget(), CellWidget(), CellWidget()
        cells.pack_start(c1, expand, fill, 0)
        cells.pack_start(CellVerticalSpacerWidget(), expand, fill, 0)
        cells.pack_start(c2, expand, fill, 0)
        cells.pack_start(CellVerticalSpacerWidget(), expand, fill, 0)
        cells.pack_start(c3, expand, fill, 0)
        c1.set_index(1)
        c2.set_index(2)
        c3.set_index(3)
        cells.show_all()


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

