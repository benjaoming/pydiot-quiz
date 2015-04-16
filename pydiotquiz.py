#!/usr/bin/env python
from gi.repository import Gtk

import pyaudio
from gi.overrides.GLib import idle_add
from thread import start_new_thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2

p = pyaudio.PyAudio()


class Handler:
    
    def __init__(self, get_object):
        self.team1_sound = None
        self.team2_sound = None
        self.team3_sound = None
        self.get_object = get_object
        self.stop_recording = False
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")
    
    def on_gamearea_button_press_event(self, area, event):
        if event.button == 1:
            start_new_thread(self.play_stream, (self.team1_sound,))
            print("TEAM 1")
        elif event.button == 2:
            print("TEAM 2")
            start_new_thread(self.play_stream, (self.team2_sound,))
        elif event.button == 3:
            print("TEAM 3")
            start_new_thread(self.play_stream, (self.team3_sound,))
    
    def on_stop_recording(self, button, *args):
        self.stop_recording = True
        self.get_object("soundteam1").set_sensitive(True)
        self.get_object("soundteam2").set_sensitive(True)
        self.get_object("soundteam3").set_sensitive(True)
        self.get_object("playteam1").set_sensitive(True)
        self.get_object("playteam2").set_sensitive(True)
        self.get_object("playteam3").set_sensitive(True)
    
    def on_record_team1(self, button, *args):
        self.record_team("team1_sound")
        
    def on_record_team2(self, button, *args):
        self.record_team("team2_sound")

    def on_record_team3(self, button, *args):
        self.record_team("team3_sound")

    def record_team(self, attr_name):
        
        self.get_object("soundteam1").set_sensitive(False)
        self.get_object("soundteam2").set_sensitive(False)
        self.get_object("soundteam3").set_sensitive(False)
        self.get_object("playteam1").set_sensitive(False)
        self.get_object("playteam2").set_sensitive(False)
        self.get_object("playteam3").set_sensitive(False)
        
        def recording_thread():
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            output_list = []
            setattr(self, attr_name, output_list)
            print("Recording to " + attr_name)
            while not self.stop_recording:
                output_list += stream.read(CHUNK)
            
            self.stop_recording = False
            print("Stopped recording " + attr_name)
        
        start_new_thread(recording_thread, ())
        
    def play_stream(self, sound_bytes):
        stream = p.open(
            output=True,
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
        )
        stream.write("".join(sound_bytes))
        stream.start_stream()
        
        stream.stop_stream()
        stream.close()
    
    def on_play_team1(self, button, *args):
        if not self.team1_sound:
            print("No team 1 sound")
            return

        start_new_thread(self.play_stream, (self.team1_sound,))
        
    def on_play_team2(self, button, *args):
        if not self.team2_sound:
            print("No team 2 sound")
            return

        start_new_thread(self.play_stream, (self.team2_sound,))

    def on_play_team3(self, button, *args):
        if not self.team3_sound:
            print("No team 3 sound")
            return

        start_new_thread(self.play_stream, (self.team3_sound,))

class IdiotQuiz:
    """This is an Hello World GTK application"""

    def __init__(self):
        
        # Set the Glade file
        builder = Gtk.Builder()
        builder.add_from_file("main_window.glade")
        builder.connect_signals(Handler(builder.get_object))
        
        # Get the Main Window, and connect the "destroy" event
        self.window = builder.get_object("window1")
        self.window.show_all()
        self.objects = builder.get_objects()


if __name__ == "__main__":
    idiotquiz = IdiotQuiz()
    Gtk.main()