"""
Code Completion for GtkSourceView
"""

from gi.repository import GObject, Gtk, GtkSource



class SageCompletionProvider(GObject.Object, GtkSource.CompletionProvider):

    __gtype_name__ = 'SageCompletionProvider'

    def __init__(self):
        GObject.Object.__init__(self)

        self.priority = 1

        theme = Gtk.IconTheme.get_default()
        icon = theme.load_icon(Gtk.STOCK_DIALOG_INFO, 16, 0)

        self.proposals = []
        self.proposals.append(GtkSource.CompletionItem.new("Proposal 1", "Proposal 1", icon, None))
        self.proposals.append(GtkSource.CompletionItem.new("Proposal 2", "Proposal 2", icon, None))
        self.proposals.append(GtkSource.CompletionItem.new("Proposal 3", "Proposal 3", icon, None))

        self.current = None

    def do_get_name(self):
        return "Sage Autocompletion"

    def do_get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def do_match(self, context):
        return True

    def do_populate(self, context):
        print('do_populate', self.current)
        self.current = context
        context.connect('cancelled', self.on_cancelled)
        context.add_proposals(self, self.proposals, True)

    def on_cancelled(self, context):
        print('cancelled', context, self.current)


GObject.type_register(SageCompletionProvider)
