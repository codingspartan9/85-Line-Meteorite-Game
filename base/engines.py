from base.history_keeper import HistoryKeeper


class CollisionsEngine:
    def is_length_collision(self, object1, object2):
        return object1.left_edge <= object2.right_edge and object1.right_edge >= object2.left_edge

    def is_height_collision(self, object1, object2):
        return object1.top_edge <= object2.bottom_edge and object1.bottom_edge >= object2.top_edge

    def is_collision(self, object1, object2):
        return self.is_length_collision(object1, object2) and self.is_height_collision(object1, object2)

    def is_type_collision(self, bigger_coordinate_object, smaller_coordinate_object, bigger_coordinate_name, smaller_coordinate_name):
        prev_bigger_coordinate_object = HistoryKeeper.get_last(bigger_coordinate_object.name)
        prev_smaller_coordinate_object = HistoryKeeper.get_last(smaller_coordinate_object.name)

        return (self.is_type_collision(bigger_coordinate_object, smaller_coordinate_object) and
                prev_bigger_coordinate_object.__dict__[bigger_coordinate_name] > prev_smaller_coordinate_object.__dict__[smaller_coordinate_name] and
                bigger_coordinate_name.__dict__[bigger_coordinate_name] <= smaller_coordinate_object.__dict__[smaller_coordinate_name])

    def is_left_collision(self, object1, object2):
        return self.is_type_collision(object1, object2, "left_edge", "right_edge")

    def is_right_collision(self, object1, object2):
        return self.is_type_collision(object2, object1, "left_edge", "right_edge")

    def is_top_collision(self, object1, object2):
        return self.is_type_collision(object2, object1, "top_edge", "bottom_edge")

    def is_bottom_collision(self, object1, object2):
        return self.is_type_collision(object1, object2, "top_edge", "bottom_edge")