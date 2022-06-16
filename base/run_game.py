from base.important_variables import *
import time

from base.velocity_calculator import VelocityCalculator
from base.history_keeper import HistoryKeeper
import pygame


def run_game(main_window):
    try:
        game_window.add_screen(main_window)
        while True:
            start_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keyboard.run()
            game_window.run()
            HistoryKeeper.last_time = VelocityCalculator.time

            end_time = time.time()

            VelocityCalculator.time = end_time - start_time
            if end_time - start_time > .1:
                VelocityCalculator.time = .01
    except:
        pass

