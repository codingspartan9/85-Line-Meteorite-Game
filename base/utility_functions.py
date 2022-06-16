import pygame.image

from base.important_variables import keyboard, game_window


def key_is_pressed(pygame_key_index):
    return keyboard.get_key_event(pygame_key_index).happened_this_cycle


def key_is_hit(pygame_key_index):
    return not keyboard.get_key_event(pygame_key_index).happened_last_cycle() and key_is_pressed(pygame_key_index)


def key_has_been_released(pygame_key_index):
    return keyboard.get_key_event(pygame_key_index).happened_last_cycle() and not key_is_pressed(pygame_key_index)


def get_time_of_key_being_held_in(pygame_key_index):
    return keyboard.get_timed_event(pygame_key_index).current_time


def mouse_is_clicked():
    return keyboard.mouse_clicked_event.is_click()


def render_image(path_to_image, left_edge, top_edge, length, height):
    image = pygame.transform.scale(pygame.image.load(path_to_image), (int(length), int(height)))
    game_window.get_window().blit(image, (left_edge, top_edge))


def get_index_of_range(range_lengths, number):
    index = -1
    start_time = 0

    for x in range(len(range_lengths)):
        range_length = range_lengths[x]
        end_time = start_time + range_length

        if number >= start_time and number <= end_time:
            index = x

        start_time = end_time

    return index


