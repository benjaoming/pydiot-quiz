#!/usr/bin/env python
from gi.repository import Gtk

import pyaudio
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2

p = pyaudio.PyAudio()


class Handler:
    
    def __init__(self):
        self.team1_sound = None
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")
    
    def on_gamearea_button_press_event(self, area, event):
        if event.button == 1:
            self.play_team1()
            print("TEAM 1")
        elif event.button == 2:
            print("TEAM 2")
        elif event.button == 3:
            print("TEAM 3")
            
    def record_team1(self, button, *args):
        self.team1_stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        self.team1_sound = []
        print("Recording Team 1")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            self.team1_sound += self.team1_stream.read(CHUNK)
            
        print("Done recording team 1")
    
    def play_team1(self):
        if not self.team1_sound:
            print("No team 1 sound")
            return
        stream = p.open(
            output=True,
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
        )
        stream.write("".join(self.team1_sound))
        stream.start_stream()
        
        stream.stop_stream()
        stream.close()


class IdiotQuiz:
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
    idiotquiz = IdiotQuiz()
    Gtk.main()