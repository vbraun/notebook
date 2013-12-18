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


INPUT_OUTPUT_VSPACE = 10


class CellVerticalSpacerWidget(Gtk.Misc):
    __gtype_name__ = 'CellVerticalSpacerWidget'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_size_request(-1, 20)

    def do_draw(self, cr):
        # paint background
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()


class CellLabelWidget(Gtk.Label):
    __gtype_name__ = 'CellLabelWidget'
    
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_property('angle', 270)



class CellExpander(Gtk.Misc):
    __gtype_name__ = 'CellExpander'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_size_request(40, 40)

    def do_draw(self, cr):
        allocation = self.get_allocation()

        # paint background
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
       
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


    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_row_homogeneous(False)
        self.set_column_homogeneous(False)

        self.set_hexpand(True)
        self.set_vexpand(False)

        i = self._make_input()
        o = self._make_output()
        e = CellExpander()
        self.attach(e, 0, 0, 1, 2)
        self.attach(i[0], 2, 0, 1, 1)
        self.attach(i[1], 1, 0, 1, 1)
        self.attach(o[0], 2, 1, 1, 1)
        self.attach(o[1], 1, 1, 1, 1)
        
        #expand = False
        #fill = False
        #self.pack_start(i, expand, fill, 0)
        #self.pack_end(o, expand, fill, 0)

    def set_index(self, i):
        self.in_label.set_text('In[{0}]'.format(i))
        self.out_label.set_text('Out[{0}]'.format(i))

    def _make_input(self):
        label = self.in_label = CellLabelWidget()
        view = self.in_view = GtkSource.View()
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

    def _make_output(self):
        label = self.out_label = CellLabelWidget()
        view = self.out_view = Gtk.TextView()
        buffer = self.out_buffer = Gtk.TextBuffer()
        buffer.set_text('output')
        view.set_buffer(buffer)
        fontdesc = Pango.FontDescription("monospace")
        view.modify_font(fontdesc)
        view.set_border_window_size(Gtk.TextWindowType.TOP, INPUT_OUTPUT_VSPACE)
        view.set_hexpand(True)
        view.set_vexpand(False)
        return label, view

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