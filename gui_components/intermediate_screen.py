from base.colors import black
from base.events import TimedEvent
from gui_components.screen import Screen
from gui_components.text_box import TextBox
from base.important_variables import *


class IntermediateScreen(Screen):
    text_box = None
    timed_event = None

    def __init__(self, message, length_of_message):
        self.text_box = TextBox(message, 25, background_color, black, True)
        self.text_box.number_set_dimensions(0, 0, screen_length, screen_height)
        self.timed_event = TimedEvent(length_of_message)

    def display(self, message=None, length_of_message=None):
        self.text_box.text = message if message is not None else self.text_box.text
        self.timed_event.time_needed = length_of_message if length_of_message is not None else self.timed_event.time_needed
        self.timed_event.start()

    def run(self):
        self.timed_event.run(self.timed_event.current_time > self.timed_event.time_needed, False)

    def get_components(self):
        return [self.text_box]
