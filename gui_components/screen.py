from gui_components.component import Component
from base.utility_functions import render_image

class Screen(Component):
    components = []
    path_to_background_file = ""

    def __init__(self, path_to_background_file=""):
        self.path_to_background_file = path_to_background_file

    def run(self):
        pass

    def get_components(self):
        return self.components

    def render_background(self):
        if self.path_to_background_file != "":
            render_image(self.path_to_background_file, self.left_edge, self.top_edge, self.length, self.height)