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
    font-size: 80%;
}}

#{cells} * GtkTextView {{
}}

#{cells} * CellExpander,
#{cells} * CellLabelWidget,
#{cells} CellVerticalSpacerWidget {{
    background-color: @theme_base_color;
}}

#{cells} * CellExpander:backdrop,
#{cells} * CellLabelWidget:backdrop,
#{cells} CellVerticalSpacerWidget:backdrop {{
    background-image: none;
    background-color: @theme_unfocused_base_color;
    box-shadow: none;
    transition: all 200ms ease-out;
}}

#{cells} * GtkSourceView {{
}}

#{cells} CellLabelWidget {{
    color: grey;
    font-size: 90%;
}}

#{cells} CellVerticalSpacerWidget:prelight {{
    background-color: lightblue;
    transition: all 500ms ease-out;
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
        view.set_name(DESCRIPTION_VIEW)
        #font_description = Pango.FontDescription('Lucida Sans 10')
        #view.modify_font(font_description)
        view.set_border_window_size(Gtk.TextWindowType.BOTTOM, 10)

    def _init_cells(self, cells):
        self.cells_view = cells
        self.cells_model = []
        cells.set_name(CELLS)
        self._add_spacer()
        cells.show()

    def _add_spacer(self):
        """
        Add a spacer to the cells view
        """
        expand = False
        fill = True
        view = self.cells_view
        spacer_cb = self.on_notebook_spacer_button_press_event
        spacer = CellVerticalSpacerWidget(spacer_cb)
        view.pack_start(spacer, expand, fill, 0)
        spacer.show()

    def _resize(self, n_cells):
        view = self.cells_view
        model = self.cells_model
        expand = False
        fill = True
        key_cb = self.on_notebook_cell_key_press_event
        missing = n_cells - len(model)
        for i in range(missing):
            c = CellWidget(key_cb)
            model.append(c)
            view.pack_start(c, expand, fill, 0)
            self._add_spacer()
        if missing < 0:
            delete_cell_from = model[missing]
            cells = view.get_children()
            pos = cells.index(delet_cell_from)
            for cell in cells[pos:]:
                view.remove(cell)
        
    def set_worksheet(self, worksheet):
        """
        Switch display to the worksheet.

        INPUT:

        - ``worksheet`` -- A
          :class:`~sage_notebok.model.worksheet.Worksheet`.
        """
        self._resize(worksheet.n_cells())
        view = self.cells_view
        model = self.cells_model
        for widget, cell in zip(model, worksheet):
            widget.update(cell)
        view.show()

    def find_cell_widget(self, cell):
        for widget in self.cells_model:
            if widget.id == cell.id:
                return widget
        raise IndexError('no widget for cell')

    def cell_busy(self, cell):
        """
        Update the view of the cell to display a running computation.
        """
        widget = self.find_cell_widget(cell)
        widget.set_output(cell)

    def cell_update(self, cell):
        """
        Update the view of the cell to display a partial result.
        """
        widget = self.find_cell_widget(cell)
        widget.set_output(cell)
        
    def cell_finished(self, cell):
        """
        Update the view of the cell to display the final result
        """
        widget = self.find_cell_widget(cell)
        widget.set_output(cell)
        
    def on_notebook_cell_key_press_event(self, widget, event):
        focus = self.cells_view.get_focus_child()
        if not isinstance(focus, CellWidget):
            return False
        if (event.keyval == Gdk.KEY_Up) and \
           not (event.state & Gdk.ModifierType.MODIFIER_MASK):
            return self._move_cursor_up(focus)
        if (event.keyval == Gdk.KEY_Down) and \
           not (event.state & Gdk.ModifierType.MODIFIER_MASK):
            return self._move_cursor_down(focus)
        if (event.keyval == Gdk.KEY_Return) and \
           (event.state & Gdk.ModifierType.CONTROL_MASK):
            cell_id = focus.id
            input_string = focus.get_input()
            self.on_notebook_evaluate_cell(cell_id, input_string)
            return True
        return False

    def on_notebook_spacer_button_press_event(self, widget, event):
        print('click ' + str(widget) + ' '+ str(event))

    def _move_cursor_up(self, cell):
        pos = self.cells_model.index(cell)
        x, y = cell.get_cursor_position()
        if not (y == 0 and pos > 0):
            return False
        prev_cell = self.cells_model[pos-1]
        prev_cell.in_view.grab_focus()
        buf = prev_cell.in_buffer
        cursor = buf.get_iter_at_line(buf.get_line_count() - 1)
        cursor.forward_chars(x)
        buf.place_cursor(cursor)
        return True

    def _move_cursor_down(self, cell):
        pos = self.cells_model.index(cell)
        x, y = cell.get_cursor_position()
        if not (y == cell.in_buffer.get_line_count()-1 and
                pos < len(self.cells_model)-1):
            return False
        next_cell = self.cells_model[pos+1]
        next_cell.in_view.grab_focus()
        buf = next_cell.in_buffer
        cursor = buf.get_iter_at_line(0)
        cursor.forward_chars(x)
        buf.place_cursor(cursor)
        return True

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


    def on_notebook_menu_cut_activate(self, widget, data=None):
        self.presenter.show_error(self, 'cut', "todo: cut")

    def on_notebook_menu_copy_activate(self, widget, data=None):
        self.presenter.show_error(self, 'copy', "todo: copy")
        
    def on_notebook_menu_paste_activate(self, widget, data=None):
        self.presenter.show_error(self, 'paste', "todo: paste")

    def on_notebook_menu_delete_activate(self, widget, data=None):
        self.presenter.show_error(self, 'delete', "todo: delete")


    def on_notebook_menu_about_activate(self, widget, data=None):
        self.presenter.show_about_window()

