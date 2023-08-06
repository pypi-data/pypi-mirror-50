import gi
gi.require_version("Gtk", '3.0')
gi.require_version("Gdk", '3.0')
from gi.repository import Gdk, Gtk

from random import randrange

class GetNames:
    MIN_NAMES = 4

    def __init__(self, window, next_button):
        self.window = window
        self.entries = []
        self.fields = Gtk.VBox()
        self.button = next_button
        self.button.set_sensitive(False)
        self.button.connect("clicked", self.on_next)
        self.add_name()
        self.add_name()
        self.add_name()
        self.add_name()
        self.vbox = Gtk.VBox()
        self.vbox.pack_start(self.fields, False, False, 0)
        self.vbox.show_all()
        self()

    def __call__(self):
        child = self.window.get_child()
        if child:
            self.window.remove(child)
        self.window.add(self.vbox)
        if hasattr(self, "names"):
            self.entries[-1].grab_focus()
        else:
            self.entries[0].grab_focus()
        Gtk.main()
        return self

    def add_name(self, entry=None):
        if entry is None or self.get_position(entry) == len(self.entries) - 1:
            hbox = Gtk.HBox()
            ev = Gtk.EventBox()
            entry = Gtk.Entry()
            ev.add(entry)
            entry.connect("activate", self.on_activate)
            entry.connect("key-press-event", self.on_key)
            entry.connect("notify::text", lambda w,*a: self.on_key(w))
            self.entries.append(entry)
            label = Gtk.Label("Name _{}: ".format(len(self.entries)))
            label.set_pattern("     _")
            label.set_use_underline(True)
            wid = Gtk.Button()
            wid.set_no_show_all(True)
            wid.connect("mnemonic-activate", self.on_mnemonic)
            label.set_mnemonic_widget(wid)
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(wid, False, False, 0)
            hbox.pack_start(ev, False, False, 0)
            self.fields.pack_start(hbox, False, False, 0)
            hbox.show_all()
        else:
            text = self.entries[-1].get_text()
            position = self.get_position(entry) + 1
            entry = self.entries[position]
            parent = entry.get_parent()
            parent.remove(entry)
            self.entries.remove(entry)
            en = Gtk.Entry()
            parent.add(en)
            en.connect("activate", self.on_activate)
            en.connect("key-press-event", self.on_key)
            en.show()
            self.entries.insert(position, en)
            prev_child = entry
            old_entry = entry
            entry = en
            old_position = position
            if position < len(self.entries) - 1:
                for position in range(position + 1, len(self.entries)):
                    next_parent = self.entries[position].get_parent()
                    child = next_parent.get_child()
                    next_parent.remove(child)
                    next_parent.add(prev_child)
                    prev_child = child
                if prev_child in self.entries: self.entries.remove(prev_child)
                self.entries.insert(old_position + 1, old_entry)
                text = child.get_text()
            self.add_name()
            self.entries[-1].set_text(text)
        self.set_next_button_sensitivity()
        entry.grab_focus()


    def get_position(self, entry):
        if type(entry) == Gtk.Entry:
            parent = entry.get_parent().get_parent()
        else:
            parent = entry.get_parent()
        return [entry.get_parent().get_parent() for entry in self.entries].index(parent)

    def on_activate(self, entry, *a):
        position = self.get_position(entry)
        if position < (len(self.entries) - 1):
            self.entries[position + 1].grab_focus()
        else:
            self.add_name()

    def on_key(self, widget, event=None):
        if event is not None and event.keyval == Gdk.KEY_Escape:
            self.remove_name(widget)
        elif event is not None and event.keyval in (Gdk.KEY_KP_Add, Gdk.KEY_plus):
            self.add_name(widget)
        self.set_next_button_sensitivity()

    def on_mnemonic(self, widget, *a):
        position = self.get_position(widget)
        self.entries[position].grab_focus()

    def on_next(self, button):
        self.names = []
        for entry in self.entries:
            name = entry.get_text().strip()
            if name:
                self.names.append(name[0].capitalize() + name[1:])
        self.names.sort()
        Gtk.main_quit()

    def remove_name(self, entry):
        if len(self.entries) <= self.MIN_NAMES: return
        focus_widget = next(e for e in self.entries if e.has_focus())
        position = self.get_position(entry)
        parent = self.entries[position].get_parent()
        self.entries[position].destroy()
        del self.entries[position]
        for position in range(position, len(self.entries)):
            next_parent = self.entries[position].get_parent()
            next_parent.remove(self.entries[position])
            parent.add(self.entries[position])
            parent = next_parent
        hbox = parent.get_parent()
        self.fields.remove(hbox)
        hbox.destroy()
        if focus_widget is None or focus_widget not in self.entries:
            focus_widget = self.entries[-1]
        if not focus_widget.has_focus(): focus_widget.grab_focus()

    def set_next_button_sensitivity(self):
        try:
            entry_texts = [entry.get_text() for entry in self.entries]
            entry_texts = [text for text in entry_texts if text]
            self.button.set_sensitive(len(entry_texts) == len(set(entry_texts)) >= self.MIN_NAMES)
        except:
            self.button.set_sensitive(False)



class GiveNames:
    def __init__(self, window, next_button, names):
        self.window = window
        self.names = names
        self.vbox = Gtk.VBox()
        self.buttons = []
        self.aliases = self.shuffle(names)
        for i in range(len(self.names)):
            self.add_name(self.names[i], self.aliases[i])

        next_button.connect("clicked", Gtk.main_quit)
        self.vbox.show_all()
        self.window.remove(self.window.get_child())
        self.window.add(self.vbox)
        Gtk.main()

    def add_name(self, name, alias):
        button = Gtk.Button(name)
        button.connect("pressed", self.on_button_press)
        button.connect("released", self.on_button_release)
        self.buttons.append(button)
        self.vbox.pack_start(button, False, False, 0)

    def on_button_press(self, button):
        button.set_label(self.aliases[self.buttons.index(button)])

    def on_button_release(self, button):
        button.set_label(self.names[self.buttons.index(button)])

    @staticmethod
    def swap(xs, a, b):
        xs[a], xs[b] = xs[b], xs[a]

    @classmethod
    def shuffle(cls, names):
        names = list(names)
        for i in range(1, len(names)):
            cls.swap(names, i, randrange(i))

        return names


def main():
    window = Gtk.Window()
    window.set_title("Couch")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("destroy", Gtk.main_quit)
    window.connect("destroy", exit)
    vbox = Gtk.VBox()
    window.add(vbox)
    container = Gtk.Alignment()
    vbox.pack_start(container, True, True, 0)
    hbox = Gtk.HBox()
    vbox.pack_end(hbox, False, False, 0)
    next_button = Gtk.Button.new_with_mnemonic("_Next")
    hbox.pack_end(next_button, False, False, 0)
    window.show_all()
    ask_widget = GetNames(container, next_button)
    GiveNames(container, next_button, ask_widget.names)
    while True:
        GiveNames(container, next_button, ask_widget().names)
    


if __name__ == '__main__':
    main()
