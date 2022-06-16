from base.dimensions import Dimensions
from base.important_variables import *
from base.utility_functions import mouse_is_clicked, render_image


class Component(Dimensions):
    color = (0, 0, 0)
    is_visible = True
    path_to_image = ""

    def __init__(self, path_to_image=""):
        self.path_to_image = path_to_image

    def run(self):
        pass

    def render(self):
        if self.path_to_image == "":
            pygame.draw.rect(game_window.get_window(), self.color, (self.left_edge, self.top_edge, self.length, self.height))

        else:
            render_image(self.path_to_image, self.left_edge, self.top_edge, self.length, self.height)

    def got_clicked(self):
        area = pygame.Rect(self.left_edge, self.top_edge, self.length, self.height)
        mouse_left_edge, mouse_top_edge = pygame.mouse.get_pos()

        return mouse_is_clicked() and area.collidepoint(mouse_left_edge, mouse_top_edge)
