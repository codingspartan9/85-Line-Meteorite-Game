from base.important_variables import screen_length, screen_height


class Dimensions:
    left_edge = 0
    top_edge = 0
    length = 0
    height = 0

    def __init__(self, left_edge, top_edge, length, height):
        self.left_edge, self.top_edge = left_edge, top_edge
        self.length, self.height = length, height

    @property
    def right_edge(self):
        return self.left_edge + self.length

    @property
    def bottom_edge(self):
        return self.top_edge + self.height

    @property
    def horizontal_midpoint(self):
        return self.left_edge + self.length / 2

    @property
    def vertical_midpoint(self):
        return self.top_edge + self.height / 2

    def number_set_dimensions(self, left_edge, top_edge, length, height):
        self.left_edge, self.top_edge = left_edge, top_edge
        self.length, self.height = length, height

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height):
        length_number = screen_length / 100
        height_number = screen_height / 100

        self.left_edge = percent_right * length_number
        self.top_edge = percent_down * height_number
        self.length = percent_length * length_number
        self.height = percent_height * height_number




