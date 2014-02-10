"""
Code Completion for GtkSourceView
"""

from gi.repository import GObject, Gtk, GtkSource



AUTOCOMPLETE_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_%.'


class SageCompletionProposal(GObject.Object, GtkSource.CompletionProposal):
    
    __gtype_name__ = 'SageCompletionProposal'
    
    def __init__(self, base, completion):
        self.base = base
        self.completion = completion
        self.label = completion
        self.markup = completion
        super(SageCompletionProposal, self).__init__()

    def do_get_label(self):
        return self.label
    
    def do_get_markup(self):
        return self.markup

    def do_get_icon(self):
        return None

    def do_get_info(self):
        return None



class SageCompletionProvider(GObject.Object, GtkSource.CompletionProvider):

    __gtype_name__ = 'SageCompletionProvider'

    def __init__(self, cell_widget):
        GObject.Object.__init__(self)
        self.cell_widget = cell_widget
        self.priority = 1
        theme = Gtk.IconTheme.get_default()
        self.icon = theme.load_icon(Gtk.STOCK_DIALOG_INFO, 16, 0)
        self.counter = 0
        self.context = None

    def do_get_name(self):
        return "Sage Autocompletion"

    def do_get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def do_match(self, context):
        ti = context.get_iter()
        rc = ti.backward_char()
        if rc is False:
            return False
        ch = ti.get_char()
        return ch in AUTOCOMPLETE_CHARS

    def do_populate(self, context):
        self.counter += 1
        self.context = context
        ti = context.get_iter()
        buf = ti.get_buffer()
        line_start = buf.get_iter_at_line(ti.get_line())
        line_end = line_start.copy()
        line_end.forward_line()
        line = buf.get_text(line_start, line_end, False)
        pos = ti.get_line_index()
        self.cell_widget.on_populate_code_completion(line, pos, self.counter)
        print('do_populate', line.strip(), pos, self.counter)

    def do_cancelled(self, context):
        print('cancelled')
        self.context = None

    def do_activate_proposal(self, proposal, text_iter):
        print('activate_proposal')
        if not isinstance(proposal, SageCompletionProposal):
            return False
        buf = text_iter.get_buffer()
        start_iter = text_iter.copy()
        start_iter.backward_chars(len(proposal.base))
        buf.delete(start_iter, text_iter)
        buf.insert(text_iter, proposal.completion)
        return True

    def populate_finish(self, base, completions, label):
        print('populate_finish', label, self.counter)
        if label != self.counter:
            return
        proposals = []
        for completion in completions:
            proposals.append(SageCompletionProposal(base, completion))
        self.context.add_proposals(self, proposals, True)


GObject.type_register(SageCompletionProposal)
GObject.type_register(SageCompletionProvider)
