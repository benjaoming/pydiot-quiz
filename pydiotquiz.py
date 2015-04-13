#!/usr/bin/env python
from gi.repository import Gtk


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")


class HellowWorldGTK:
    """This is an Hello World GTK application"""

    def __init__(self):
        
        # Set the Glade file
        builder = Gtk.Builder()
        builder.add_from_file("main_window.glade")
        builder.connect_signals(Handler())
        
        # Get the Main Window, and connect the "destroy" event
        self.window = builder.get_object("window1")
        self.window.show_all()
        self.objects = builder.get_objects()


if __name__ == "__main__":
    hwg = HellowWorldGTK()
    Gtk.main()