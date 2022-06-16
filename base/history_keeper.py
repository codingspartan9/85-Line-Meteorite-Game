from copy import deepcopy

from base.velocity_calculator import VelocityCalculator


class HistoryKeeper:
    last_objects = {}
    last_time = 0

    def add(name, history_keeper_object, needs_deepcopy):
        if needs_deepcopy:
            history_keeper_object = deepcopy(history_keeper_object)

        HistoryKeeper.last_objects[f"{name}{VelocityCalculator.time}"] = history_keeper_object

    def get_last(name):
        return HistoryKeeper.last_objects.get(f"{name}{HistoryKeeper.last_time}")








