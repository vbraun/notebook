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
import cairo


INPUT_OUTPUT_VSPACE = 5

class CellVerticalSpacerWidget(Gtk.EventBox):
    __gtype_name__ = 'CellVerticalSpacerWidget'

    def __init__(self, button_press_callback, *args, **kwds):
        super(CellVerticalSpacerWidget, self).__init__(*args, **kwds)
        self.set_size_request(-1, 10)
        self.connect('enter-notify-event', self.on_enter_notify_event)
        self.connect('leave-notify-event', self.on_leave_notify_event)
        self.connect('button-press-event', button_press_callback)

    def do_draw(self, cr):
        context = self.get_style_context() 
        allocation = self.get_allocation() 
        Gtk.render_frame(context, cr, 0, 0, 
                         allocation.width, allocation.height) 
        
    def on_enter_notify_event(self, widget, event):
        widget.set_state(Gtk.StateFlags.PRELIGHT)
        
    def on_leave_notify_event(self, widget, event): 
        widget.set_state(Gtk.StateFlags.NORMAL) 


class CellLabelWidget(Gtk.Label):
    __gtype_name__ = 'CellLabelWidget'
    
    def __init__(self, *args, **kwds):
        super(CellLabelWidget, self).__init__(*args, **kwds)
        #self.set_property('angle', 270)

class CellExpander(Gtk.Misc):
    __gtype_name__ = 'CellExpander'

    def __init__(self, *args, **kwds):
        super(CellExpander, self).__init__(*args, **kwds)
        self.set_size_request(40, -1)

    def do_draw(self, cr):
        context = self.get_style_context() 
        allocation = self.get_allocation()
        Gtk.render_background(context, cr, 0, 0, 
                              allocation.width, allocation.height) 

        # # draw a diagonal line
        # allocation = self.get_allocation()
        # fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        # cr.set_source_rgba(*list(fg_color));
        # cr.set_line_width(2)
        # cr.move_to(0, 0)   # top left of the widget
        # cr.line_to(allocation.width, allocation.height)
        # cr.stroke()

        glyph_top = u'\u23a7'
        glyph_mid = u'\u23a8'
        glyph_bot = u'\u23a9'
        glyph_stretch = u'\u23aa'

        #cr.select_font_face('monospace',
        #                    cairo.FONT_SLANT_NORMAL,
        #                    cairo.FONT_WEIGHT_BOLD)

        fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(fg_color));
        cr.set_font_size(18)
        x_pos = 20
        y_pad = 0
        y_pos = 0 + y_pad
        brace_height = allocation.height - 2*y_pad
        x_bearing, y_bearing, top_width, top_height = cr.text_extents(glyph_top)[:4]
        if 2.1 * top_height > allocation.height:
            # parts would run into each other
            return
        top_y = y_pos + 0
        cr.move_to(x_pos, top_y - y_bearing)
        cr.show_text(glyph_top)

        x_bearing, y_bearing, mid_width, mid_height = cr.text_extents(glyph_mid)[:4]
        mid_y = y_pos + (brace_height-mid_height)/2.0
        cr.move_to(x_pos, mid_y - y_bearing)
        cr.show_text(glyph_mid)

        x_bearing, y_bearing, bot_width, bot_height = cr.text_extents(glyph_bot)[:4]
        bot_y = y_pos + (brace_height - bot_height)
        cr.move_to(x_pos, bot_y - y_bearing)
        cr.show_text(glyph_bot)

        overlap = 2
        x_bearing, y_bearing, stretch_width, stretch_height = \
            cr.text_extents(glyph_stretch)[:4]
        # vertical space to fill with the stretched character
        desired = (brace_height - top_height - mid_height - bot_height)/2 + 2*overlap
        desired *= 1.02   # why? get gaps in long cells
        m = cr.get_font_matrix()
        scale = desired / stretch_height
        m.scale(1.0, scale)
        cr.set_font_matrix(m)
        
        cr.move_to(x_pos, 
                   top_y + top_height - scale*y_bearing - overlap)
        cr.show_text(glyph_stretch)

        cr.move_to(x_pos,
                   mid_y + mid_height - scale*y_bearing - overlap)
        cr.show_text(glyph_stretch)


        
        #cr.move_to(1 - width / 2 - x_bearing, 0.5 - height / 2 - y_bearing)

        #cr.move_to(allocation.width/2 - x_bearing - width/2, 
        # j          allocation.height/2 - y_bearing - height/2)
        #cr.show_text(bracket)
        


class CellWidget(Gtk.Grid):
    __gtype_name__ = 'CellWidget'

    def __init__(self, key_press_event_callback, *args, **kwds):
        self._key_press_event_callback = key_press_event_callback
        super(CellWidget, self).__init__(*args, **kwds)
        self.set_row_homogeneous(False)
        self.set_column_homogeneous(False)

        self.set_hexpand(True)
        self.set_vexpand(False)

        i = self._make_input()
        o = self._make_output()
        e = CellExpander()
        e.show()
        self.attach(e,    0, 0, 1, 2)
        self.attach(i[0], 2, 0, 1, 1)
        self.attach(i[1], 1, 0, 1, 1)
        self.attach(o[0], 2, 1, 1, 1)
        self.attach(o[1], 1, 1, 1, 1)
        
        #expand = False
        #fill = False
        #self.pack_start(i, expand, fill, 0)
        #self.pack_end(o, expand, fill, 0)

    def set_index(self, index):
        if index is None:
            self.in_label.hide()
            self.out_label.hide()
        else:
            self.in_label.set_text('In[{0}]'.format(index))
            self.out_label.set_text('Out[{0}]'.format(index))
            self.in_label.show()
            self.out_label.show()

    def _make_input(self):
        label = self.in_label = CellLabelWidget()
        view = self.in_view = GtkSource.View()
        view.connect("key_press_event", self._key_press_event_callback)
        buffer = self.in_buffer = GtkSource.Buffer()
        style = GtkSource.StyleSchemeManager().get_scheme('tango')
        buffer.set_style_scheme(style)
        buffer.set_text('def f(x):\n    return 1')
        view.set_buffer(buffer)
        # fontdesc = Pango.FontDescription("monospace")
        fontdesc = Pango.FontDescription("Consolas 12")
        view.modify_font(fontdesc)
        self.set_language()
        view.set_hexpand(True)
        view.set_vexpand(False)
        return label, view

    def set_input(self, input_string):
        self.in_buffer.set_text(input_string)
        self.in_view.show()
        
    def get_input(self):
        buf = self.in_buffer
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)

    def _make_output(self):
        label = self.out_label = CellLabelWidget()
        view = self.out_view = Gtk.TextView()
        buffer = self.out_buffer = Gtk.TextBuffer()
        buffer.set_text('output')
        view.set_buffer(buffer)
        fontdesc = Pango.FontDescription("monospace")
        view.modify_font(fontdesc)
        #view.set_border_window_size(Gtk.TextWindowType.TOP, INPUT_OUTPUT_VSPACE)
        view.set_hexpand(True)
        view.set_vexpand(False)
        view.set_cursor_visible(False)
        view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        return label, view

    def set_output(self, cell):
        self.set_index(cell.index)
        output = cell.as_plain_text()
        self.out_buffer.set_text(output)
        if len(output.strip()) > 0:
            self.out_view.show()
        else:
            self.out_view.hide()
            self.out_label.hide()
        
    def set_language(self, language='python'):
        mgr = GtkSource.LanguageManager()
        lang = mgr.get_language(language)
        self.in_buffer.set_language(lang)
        view = self.in_view
        view.set_insert_spaces_instead_of_tabs(True)
        view.set_tab_width(4)
        view.set_auto_indent(True)
        #view.set_show_line_numbers(True)
        view.set_show_right_margin(False)

    def update(self, cell):
        """
        Update view to display ``cell``

        This must be called at least once before the cell is actually
        displayed. On subsequent calls, it replaces all data from the
        previous cell. This allows you to reuse :class:`CellWidget`
        instances.

        INPUT:

        - ``cell`` -- a (potentially) entirely different notebook
          cell.
        """
        self.set_index(cell.index)
        self.set_input(cell.input)
        self.set_output(cell)
        self._id = cell.id
        self.show()

    @property
    def id(self):
        return self._id
    
    def get_cursor_position(self):
        """
        Return the column/row position of the cursor in the input area
        """
        buf = self.in_buffer
        cursor = buf.get_iter_at_mark(buf.get_insert())
        x = cursor.get_line_offset()
        y = cursor.get_line()
        return (x, y)
