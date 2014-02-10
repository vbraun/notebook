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

MENU_INSERT_BEFORE = 'notebook_menu_insert_before'
MENU_INSERT_AFTER = 'notebook_menu_insert_after'
MENU_CELL_DELETE = 'notebook_menu_cell_delete'

TOOLBUTTON_RUN = 'notebook_toolbutton_run'
TOOLBUTTON_STOP = 'notebook_toolbutton_stop'
TOOLBUTTON_SPINNER = 'notebook_toolbutton_spinner'


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
    background-color: #BCECAC;
    transition: all 500ms ease-out;
}}

#{cells} *:insensitive {{
    background-color: #BCECAC;
    transition: all 500ms ease-out;
}}
""".format(
    window=WINDOW, 
    title=TITLE, 
    description=DESCRIPTION_VIEW,
    cells=CELLS
).encode('utf-8')



class CellsModel(object):

    def __init__(self):
        """
        Container for the cell widgets
        """
        self._data = []

    def __iter__(self):
        for widget in self._data:
            yield widget

    def __len__(self):
        return len(self._data)

    def __getitem__(self, pos):
        return self._data[pos]

    def append(self, widget):
        self._data.append(widget)

    def index(self, widget):
        return self._data.index(widget)

    def remove(self, widget):
        self._data.remove(widget)

    def find(self, cell):
        """
        Find the widget displaying the given cell

        INPUT:

        - ``cell`` -- a cell of the notebook data model
        """
        for widget in self._data:
            if widget.id == cell.id:
                return widget
        raise IndexError('no widget for cell')
        
    def find_prev_sensitive(self, cell):
        """
        Find the previous cells' widget, skipping over insensitive widgets

        INPUT:

        - ``cell`` -- a cell of the notebook data model

        OUTPUT:

        The widget preceeding the cell's widget (ignoring insensitive
        widgets), or ``None`` if there is no such widget.
        """            
        pos = self.index(cell)
        while True:
            pos = pos - 1
            if pos < 0:
                return None
            prev_cell = self[pos]
            if prev_cell.is_sensitive():
                return prev_cell

    def find_next_sensitive(self, cell):
        """
        Find the next cells' widget, skipping over insensitive widgets

        INPUT:

        - ``cell`` -- a cell of the notebook data model

        OUTPUT:

        The widget following the cell's widget (ignoring insensitive
        widgets), or ``None`` if there is no such widget.
        """            
        pos = self.index(cell)
        while True:
            pos = pos + 1
            if pos == len(self):
                return None
            next_cell = self[pos]
            if next_cell.is_sensitive():
                return next_cell



class NotebookWindowGtk(NotebookWindowABC, WindowGtk):


    def __init__(self, presenter, make_builder):
        builder = make_builder(
            WINDOW, TITLE, DESCRIPTION_VIEW, DESCRIPTION_MODEL, CELLS,
            MENU_INSERT_BEFORE, MENU_INSERT_AFTER, MENU_CELL_DELETE,
            TOOLBUTTON_RUN, TOOLBUTTON_STOP, TOOLBUTTON_SPINNER)
        WindowGtk.__init__(self, WINDOW, presenter, builder=builder)
        self.menu_insert_before = builder.get_object(MENU_INSERT_BEFORE)
        self.menu_insert_after = builder.get_object(MENU_INSERT_AFTER)
        self.menu_cell_delete = builder.get_object(MENU_CELL_DELETE)
        self.toolbutton_run = builder.get_object(TOOLBUTTON_RUN)
        self.toolbutton_stop = builder.get_object(TOOLBUTTON_STOP)
        self.toolbutton_spinner = builder.get_object(TOOLBUTTON_SPINNER)
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
        self.cells_model = CellsModel()
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
        focus_in_cb = self.on_notebook_cell_focus_in_event
        focus_out_cb = self.on_notebook_cell_focus_out_event
        complete_cb = self.on_notebook_cell_code_complete
        missing = n_cells - len(model)
        for i in range(missing):
            c = CellWidget(key_cb, focus_in_cb, focus_out_cb, complete_cb)
            model.append(c)
            view.pack_start(c, expand, fill, 0)
            self._add_spacer()
        if missing < 0:
            delete_cell_from = model[missing]
            cells = view.get_children()
            pos = cells.index(delete_cell_from)
            for cell in cells[pos:pos-2*missing]:
                view.remove(cell)
                if isinstance(cell, CellWidget):
                    model.remove(cell)
        assert n_cells == len(model)
        assert n_cells == sum(1 for child in view.get_children() if isinstance(child, CellWidget))
        
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

    def cell_grab_focus(self, cell):
        """
        Focus and place cursor into cell input area
        """
        widget = self.cells_model.find(cell)
        if widget is self.cells_view.get_focus_child():
            return
        widget.in_view.grab_focus()
        buf = widget.in_buffer
        buf.place_cursor(buf.get_start_iter())

    def cell_busy(self, cell):
        """
        Update the view of the cell to display a running computation.
        """
        self.toolbutton_stop.set_sensitive(True)
        self.toolbutton_spinner.start()
        widget = self.cells_model.find(cell)
        widget.set_output(cell)
        widget.set_sensitive(False)

    def cell_update(self, cell):
        """
        Update the view of the cell to display a (potentially partial) result.
        """
        widget = self.cells_model.find(cell)
        widget.set_output(cell)
        
    def cell_finished(self, cell):
        """
        Update the view of the cell to display the final result
        """
        widget = self.cells_model.find(cell)
        widget.set_output(cell)
        widget.set_sensitive(True)
        self.toolbutton_stop.set_sensitive(False)
        self.toolbutton_spinner.stop()
        
    def on_notebook_cell_key_press_event(self, widget, event):
        """
        Callback for keyboard entry in all cell widgets
        """
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
           (event.state & Gdk.ModifierType.SHIFT_MASK):
            return self._start_evaluate_cell(focus)
        if (event.keyval == Gdk.KEY_Delete) and \
           (event.state & Gdk.ModifierType.CONTROL_MASK):
            return self.presenter.delete_cell(focus.id)
        return False

    def _start_evaluate_cell(self, cell):
        cell_id = cell.id
        input_string = cell.get_input()
        self.on_notebook_evaluate_cell(cell_id, input_string)
        # Move cursor to the next cell, insert one if necessary
        cells = self.cells_model
        next_widget = cells.find_next_sensitive(cell)
        if next_widget is None:
            pos = len(cells)
            self.presenter.insert_cell_at(pos)
        else:
            next_widget.in_view.grab_focus()
            buf = next_widget.in_buffer
            cursor = buf.get_start_iter()
            buf.place_cursor(cursor)
        return True

    def on_notebook_cell_focus_in_event(self, widget, event):
        """
        Callback: Notebook cell got focused
        """
        self.toolbutton_run.set_sensitive(True)
        self.menu_insert_before.set_sensitive(True)
        self.menu_insert_after.set_sensitive(True)
        self.menu_cell_delete.set_sensitive(True)

    def on_notebook_cell_focus_out_event(self, widget, event):
        """
        Callback: Notebook cell lost focus
        """
        self.toolbutton_run.set_sensitive(False)
        self.menu_insert_before.set_sensitive(False)
        self.menu_insert_after.set_sensitive(False)
        self.menu_cell_delete.set_sensitive(False)

    def on_notebook_spacer_button_press_event(self, widget, event):
        pos = 0
        for child in self.cells_view.get_children():
            if isinstance(child, CellWidget):
                pos += 1
            if child is widget:
                self.presenter.insert_cell_at(pos)
                return
        raise ValueError('clicked on spacer that is not a child of the cells_view') 

    def _move_cursor_up(self, cell):
        x, y = cell.get_cursor_position()
        if not (y == 0):
            return False
        prev_cell = self.cells_model.find_prev_sensitive(cell)
        if prev_cell is None:
            return False
        prev_cell.in_view.grab_focus()
        buf = prev_cell.in_buffer
        cursor = buf.get_iter_at_line(buf.get_line_count() - 1)
        cursor.forward_chars(x)
        buf.place_cursor(cursor)
        return True

    def _move_cursor_down(self, cell):
        x, y = cell.get_cursor_position()
        if not y == cell.in_buffer.get_line_count() - 1:
            return False
        next_cell = self.cells_model.find_next_sensitive(cell)
        if next_cell is None:
            return False
        next_cell.in_view.grab_focus()
        buf = next_cell.in_buffer
        cursor = buf.get_iter_at_line(0)
        cursor.forward_chars(x)
        buf.place_cursor(cursor)
        return True

    #def on_notebook_cell_code_complete(self, input_string, cursor_pos, cell_id, context):    
    #    super(NotebookWindowGtk, self).on_notebook_cell_code_complete(
    #        input_string, cursor_pos, cell_id, context)
        
    def code_complete_finished(self, cell, completion):
        """
        Update the view to display completions
        """
        widget = self.cells_model.find(cell)
        c = completion
        widget.show_code_completions(c.base, c.completions, c.request.label)

    def on_notebook_window_delete_event(self, widget, data=None):
        self.presenter.hide_notebook_window()
        return False

    def on_notebook_window_destroy(self, widget, data=None):
        logging.info('TODO: destroyed. autosave?')
        
    def on_notebook_toolbutton_run_clicked(self, widget, data=None):
        focus = self.cells_view.get_focus_child()
        if not isinstance(focus, CellWidget):
            return False
        return self._start_evaluate_cell(focus)

    def on_notebook_toolbutton_stop_clicked(self, widget, data=None):
        self.presenter.show_notification(self, "todo: stop")

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

    def on_notebook_menu_insert_before_activate(self, widget, data=None):
        focus = self.cells_view.get_focus_child()
        if not isinstance(focus, CellWidget):
            return False
        pos = self.cells_model.index(focus)
        self.presenter.insert_cell_at(pos)

    def on_notebook_menu_insert_after_activate(self, widget, data=None):
        focus = self.cells_view.get_focus_child()
        if not isinstance(focus, CellWidget):
            return False
        focus = self.cells_view.get_focus_child()
        if not isinstance(focus, CellWidget):
            return False
        pos = self.cells_model.index(focus)
        self.presenter.insert_cell_at(pos+1)

    def on_notebook_menu_cell_delete_activate(self, widget, data=None):
        self.presenter.show_error(self, 'delete', "todo: delete")


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

