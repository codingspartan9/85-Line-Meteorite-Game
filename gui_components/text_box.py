import pygame

from base.dimensions import Dimensions
from gui_components.component import Component
from base.important_variables import game_window


class TextBox(Component):
    text = ""
    font = None
    font_size = None
    background_color = None
    text_color = None
    is_centered = False

    def __init__(self, text, font_size, background_color, text_color, is_centered):
        self.text, self.font_size = text, font_size
        self.background_color, self.text_color = background_color, text_color

        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.color = background_color
        self.is_centered = is_centered
        Dimensions.__init__(self, 0, 0, 0, 0)

    def render(self):
        super().render()

        text = self.font.render(self.text, True, self.text_color, self.background_color)
        text_rectangle = text.get_rect()

        if not self.is_centered:
            text_rectangle.top = self.top_edge
            text_rectangle.left = self.left_edge

        if self.is_centered:
            text_rectangle.center = (self.horizontal_midpoint, self.vertical_midpoint)

        game_window.get_window().blit(text, text_rectangle)







