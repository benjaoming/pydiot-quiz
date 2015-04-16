#!/usr/bin/env python
from gi.repository import Gtk  # @UnresolvedImport

import time
import pyaudio
from gi.overrides.GLib import timeout_add
from gobject import source_remove
from thread import start_new_thread
from gi.overrides.Gdk import RGBA

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2

p = pyaudio.PyAudio()


SECONDS_TO_ANSWER = [30, 20, 10]
ORDER_PRESSED = ["First", "Second", "Third"]

EMPTY_LABEL = "-"


class Handler:
    
    def __init__(self, get_object):
        self.team1_sound = None
        self.team2_sound = None
        self.team3_sound = None
        self.answer_queue_position = 0  # Order of which buttons were pushed
        self.seconds_left = 0
        self.answer_queue_labels = []
        self.reset_countdown_to = None
        self.answering_position = 0
        self.running_countdown = None
        self.team1_answered = False
        self.team2_answered = False
        self.team3_answered = False
        self.get_object = get_object
        self.stop_recording = False
    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")
    
    def on_gamearea_button_press_event(self, area, event):
        if self.answer_queue_position > 2:
            return
        if event.button == 1:
            if self.team1_answered:
                return
            self.team1_answered = True
            self.get_object("answer_order_team1").set_text(ORDER_PRESSED[self.answer_queue_position])
            self.answer_queue_labels.append(self.get_object("team1_label"))
            start_new_thread(self.play_stream, (self.team1_sound,))
            print("TEAM 1")
        elif event.button == 2:
            if self.team2_answered:
                return
            self.team2_answered = True
            self.answer_queue_labels.append(self.get_object("team2_label"))
            self.get_object("answer_order_team2").set_text(ORDER_PRESSED[self.answer_queue_position])
            print("TEAM 2")
            start_new_thread(self.play_stream, (self.team2_sound,))
        elif event.button == 3:
            if self.team3_answered:
                return
            self.team3_answered = True
            self.answer_queue_labels.append(self.get_object("team3_label"))
            self.get_object("answer_order_team3").set_text(ORDER_PRESSED[self.answer_queue_position])
            print("TEAM 3")
            start_new_thread(self.play_stream, (self.team3_sound,))
        
        self.get_object("time_next_team").set_sensitive(True)
        self.answer_queue_position += 1
    
    def on_stop_recording(self, button, *args):
        self.stop_recording = True
        self.get_object("soundteam1").set_sensitive(True)
        self.get_object("soundteam2").set_sensitive(True)
        self.get_object("soundteam3").set_sensitive(True)
        self.get_object("playteam1").set_sensitive(True)
        self.get_object("playteam2").set_sensitive(True)
        self.get_object("playteam3").set_sensitive(True)
        self.get_object("stoprecording").set_sensitive(False)
    
    def on_record_team1(self, button, *args):
        self.record_team("team1_sound")
        
    def on_record_team2(self, button, *args):
        self.record_team("team2_sound")

    def on_record_team3(self, button, *args):
        self.record_team("team3_sound")
    
    def on_reset_all(self, button, *args):
        self.answer_queue_position = 0  # Order of which buttons were pushed
        self.answer_queue_labels = []
        self.answering_position = 0
        self.team1_answered = False
        self.team2_answered = False
        self.team3_answered = False
        self.get_object("answer_order_team1").set_text(EMPTY_LABEL)
        self.get_object("answer_order_team2").set_text(EMPTY_LABEL)
        self.get_object("answer_order_team3").set_text(EMPTY_LABEL)
        self.get_object("time_next_team").set_sensitive(False)
        self.get_object("team1_label").override_background_color(0, RGBA(1, 1, 1, 0.0))
        self.get_object("team2_label").override_background_color(0, RGBA(1, 1, 1, 0.0))
        self.get_object("team3_label").override_background_color(0, RGBA(1, 1, 1, 0.0))
        self.seconds_left = 0

    def on_time_next_team(self, button, *args):
        print("Next team")
        if self.answering_position >= len(self.answer_queue_labels):
            return
        
        self.answer_queue_labels[self.answering_position].override_background_color(0, RGBA(1.0, 0.8, 0.8, 1.0))

        if self.running_countdown:
            source_remove(self.running_countdown)
        self.seconds_left = SECONDS_TO_ANSWER[self.answering_position]
        self.countdown()
        self.answering_position += 1
    
    def countdown(self,):
        if self.seconds_left <= 0:
            self.get_object("countdown").set_text("0")
            return False
        self.get_object("countdown").set_text(str(self.seconds_left))
        self.seconds_left -= 1
        self.running_countdown = timeout_add(1000, self.countdown)
    
    def record_team(self, attr_name):
        
        self.get_object("soundteam1").set_sensitive(False)
        self.get_object("soundteam2").set_sensitive(False)
        self.get_object("soundteam3").set_sensitive(False)
        self.get_object("playteam1").set_sensitive(False)
        self.get_object("playteam2").set_sensitive(False)
        self.get_object("playteam3").set_sensitive(False)
        self.get_object("stoprecording").set_sensitive(True)
        
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
            setattr(self, attr_name, output_list)
            self.stop_recording = False
            print("Stopped recording " + attr_name)
        
        start_new_thread(recording_thread, ())
        
    def play_stream(self, sound_bytes):
        if not sound_bytes:
            return
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