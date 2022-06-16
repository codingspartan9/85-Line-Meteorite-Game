import random
from base.file_reader import FileReader;from base.important_variables import *;from gui_components.intermediate_screen import IntermediateScreen;from base.run_game import run_game;from gui_components.navigation_screen import NavigationScreen;from base.lines import *;from base.colors import *;from base.dimensions import Dimensions;from base.velocity_calculator import VelocityCalculator;from base.utility_functions import *;from base.events import TimedEvent;from base.file_reader import os
from gui_components.screen import Screen;from gui_components.text_box import TextBox;from gui_components.grid import Grid;from gui_components.component import Component
class MeteoriteGameScreen(Screen):
    time_between_meteorites = Path(Point(0, 5),[Point(1000, 5), Point(1500, 4.5), Point(2000, 4), Point(2500, 3.5),Point(3500, 2.2), Point(float("inf"), 2.2)]);    time_for_meteorites_to_fall = Path(Point(0, 5),[Point(1000, 5), Point(1500, 4), Point(2000, 3.5), Point(2500, 3), Point(3500, 2), Point(float("inf"), 2)]);    points_per_meteorite_destroyed = 200;    players = [];    meteorites = [];    time_since_last_meteorite = 0;    number_of_players = 0;    player_total_score = 0;    player_scores = [];    player_score_fields = [];    high_score = 0;    high_score_field = None;    hud = [];    game_is_reset = False;    is_versus = False; intermediate_screen = None; is_high_score = False
    def __init__(self, number_of_players, is_versus):
        super().__init__("images/galaxy.png")
        Dimensions.__init__(self, 0, 0, screen_length, screen_height)
        self.is_versus = is_versus;        self.players = [];        self.meteorites = [];        self.player_score_fields = [];        self.player_scores = [];        self.number_of_players = number_of_players;        all_player_keys = [[pygame.K_d, pygame.K_a, pygame.K_f], [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SLASH]];         self.high_score_field = TextBox("", 25, pleasing_green, white, True); self.intermediate_screen = IntermediateScreen("", 2)
        self.players = [Player(all_player_keys[player_number][0], all_player_keys[player_number][1], all_player_keys[player_number][2], f"images/player{player_number + 1}.png", f"images/player{player_number + 1}_bullet.png") for player_number in range(number_of_players) if True]
        for x in range(len(self.players)):
            self.player_score_fields = self.player_score_fields + [TextBox("", 25, white, [blue, red][x], True)] if x == 0 or (x >= 1 and self.is_versus) else self.player_score_fields;                self.player_scores = self.player_scores + [0] if x == 0 or (x >= 1 and self.is_versus) else self.player_scores
        self.set_players_left_edge()
        self.hud = self.player_score_fields + [self.high_score_field]
        self.create_meteorites(self.time_for_meteorites_to_fall.get_y_coordinate(0))
        Grid(Dimensions(0, 0, screen_length, screen_height * .1), 1, None).turn_into_grid(self.hud, None, None)
    def run(self):
        self.time_since_last_meteorite = VelocityCalculator.time + self.time_since_last_meteorite;        self.game_is_reset = False;         self.high_score_field.text = f"High Score: {self.high_score}"; alive_meteorites = [];self.is_high_score = True if sorted(self.player_scores)[-1] > self.high_score else self.is_high_score;self.high_score = sorted(self.player_scores)[-1] if sorted(self.player_scores)[-1] > self.high_score else self.high_score
        self.intermediate_screen.run()
        for x in range(len(self.player_score_fields)):
            self.player_score_fields[x].text = f"Player #{x + 1}: {self.player_scores[x]}";            self.player_total_score = self.player_scores[x] + self.player_total_score if x != 0 else self.player_scores[x]
        for meteorite in self.meteorites:
            self.player_scores[meteorite.last_player_hit_by] = self.points_per_meteorite_destroyed + self.player_scores[meteorite.last_player_hit_by] if meteorite.hit_points <= 0 and self.is_versus else self.player_scores[meteorite.last_player_hit_by]; self.player_scores[0] = self.points_per_meteorite_destroyed + self.player_scores[0] if meteorite.hit_points <= 0 and not self.is_versus else self.player_scores[0]; alive_meteorites = alive_meteorites + [meteorite] if meteorite.hit_points > 0 else alive_meteorites
            for x in range(len(self.players)):
                player = self.players[x];            alive_lasers = []
                (self.reset_game if collisions_engine.is_collision(meteorite, player) or meteorite.bottom_edge >= screen_height else lambda:[])()
                for laser in player.lasers:
                    alive_lasers = alive_lasers + [laser] if laser.bottom_edge > 0 and not collisions_engine.is_collision(laser, meteorite) else alive_lasers; meteorite.hit_points -= laser.damage if collisions_engine.is_collision(laser, meteorite) else 0; meteorite.last_player_hit_by = (x if self.is_versus else 0) if collisions_engine.is_collision(laser, meteorite) else meteorite.last_player_hit_by
                player.lasers = alive_lasers
        prev_time = self.time_since_last_meteorite; self.time_since_last_meteorite = 0 if self.time_since_last_meteorite >= self.time_between_meteorites.get_y_coordinate(self.player_total_score) or (len(alive_meteorites if not self.game_is_reset else self.meteorites) == 0 and key_is_hit(pygame.K_s)) else self.time_since_last_meteorite; self.components = (self.hud + [component for player in self.players for component in player.components] + alive_meteorites if not self.game_is_reset else self.meteorites) if self.intermediate_screen.timed_event.has_finished() else self.intermediate_screen.get_components(); self.meteorites = alive_meteorites if not self.game_is_reset else self.meteorites
        (self.create_meteorites if prev_time >= self.time_between_meteorites.get_y_coordinate(self.player_total_score) or (len(self.meteorites) == 0 and key_is_hit(pygame.K_s)) else lambda number: [])(self.time_for_meteorites_to_fall.get_y_coordinate(self.player_total_score))
    def create_meteorites(self, time_for_meteorite_to_fall):
        for x in range(self.number_of_players):
            start_left_edge = random.randint(0, screen_length - Meteorite.length);        hit_points = 3
            end_left_edge = random.randint(0 if start_left_edge - screen_length / 2 < 0 else start_left_edge - screen_length / 2, screen_length - Meteorite.length if start_left_edge + screen_length / 2 > screen_length - Meteorite.length else start_left_edge + screen_length / 2 > screen_length - Meteorite.length)
            self.meteorites.append(Meteorite(LineSegment(Point(start_left_edge, -Meteorite.height), Point(end_left_edge, screen_height - Meteorite.height)), time_for_meteorite_to_fall, hit_points))
    def reset_game(self):
        self.intermediate_screen.display(self.get_versus_message() if self.is_versus else f"You Scored {self.player_scores[0]}" if not self.is_high_score else f"New High Score: {self.player_scores[0]}")
        self.is_high_score = False;self.meteorites = [];        self.game_is_reset = True;        self.player_total_score = 0;        self.time_since_last_meteorite = 0;         self.player_scores = [0] * len(self.player_scores)
        self.create_meteorites(self.time_for_meteorites_to_fall.get_y_coordinate(0))
        for player in self.players:
            player.left_edge = screen_length / 2;        player.lasers = [];        player.can_move_left, player.can_move_right = True, True
            player.wait_to_shoot_event.reset()
        self.set_players_left_edge()
    def set_players_left_edge(self):
        previous_player_left_edge = (screen_length / 2) + Player.length
        for player in self.players:
            player.left_edge = previous_player_left_edge - player.length;            previous_player_left_edge = previous_player_left_edge - player.length
    def get_versus_message(self):
        player_number_who_won = 1;current_best_score = -1;is_tie = True
        for x in range(len(self.player_scores)):
            is_tie = False if self.player_scores[x] != current_best_score and current_best_score != -1 else is_tie;player_number_who_won = x + 1 if self.player_scores[x] > current_best_score else player_number_who_won;current_best_score = self.player_scores[x] if self.player_scores[x] > current_best_score else current_best_score
        return f"Player #{player_number_who_won} Won" if not is_tie else "It was a tie"
class Player(Component):
    right_key = None;    left_key = None;    shoot_key = None;    path_to_player_image = None;    path_to_laser_image = None;    length = VelocityCalculator.get_measurement(screen_length, 15);    height = VelocityCalculator.get_measurement(screen_height, 20);    velocity = VelocityCalculator.get_velocity(screen_length, 700);    can_move_left = True;    can_move_right = True;    lasers = [];    key_hit = False;    wait_to_shoot_event = None; components = []
    def __init__(self, right_key, left_key, shoot_key, path_to_player_image, path_to_laser_image):
        Dimensions.__init__(self, screen_length / 2, screen_height - self.height, self.length, self.height)
        super().__init__(path_to_player_image)
        self.lasers = [];        self.right_key = right_key;        self.left_key = left_key;        self.shoot_key = shoot_key;        self.path_to_laser_image = path_to_laser_image;        self.wait_to_shoot_event = TimedEvent(.2); self.components = [self]
    def run(self):
        self.left_edge = (VelocityCalculator.calculate_distance(self.velocity) if key_is_pressed(self.right_key) and self.right_edge < screen_length else 0) + self.left_edge; self.left_edge = self.left_edge - (VelocityCalculator.calculate_distance(self.velocity) if key_is_pressed(self.left_key) and self.left_edge > 0 else 0); self.components = [self] + self.lasers;         self.left_edge = 0 if not self.left_edge > 0 and key_is_pressed(self.right_key) else self.left_edge;        self.left_edge = screen_length - self.length if not self.right_edge < screen_length and not key_is_pressed(self.left_key) else self.left_edge
        self.wait_to_shoot_event.run(self.wait_to_shoot_event.current_time > self.wait_to_shoot_event.time_needed, False)
        if key_has_been_released(self.shoot_key) and self.wait_to_shoot_event.has_finished():
            self.lasers.append(Laser(self.horizontal_midpoint - [1, 1.5, 2][get_index_of_range([.5, 1, float("inf")], get_time_of_key_being_held_in(self.shoot_key))] * Laser.length / 2,self.top_edge - [1, 1.5, 2][get_index_of_range([.5, 1, float("inf")], get_time_of_key_being_held_in(self.shoot_key))] * Laser.height, self.path_to_laser_image, [1, 1.5, 2][get_index_of_range([.5, 1, float("inf")], get_time_of_key_being_held_in(self.shoot_key))], get_index_of_range([.5, 1, float("inf")], get_time_of_key_being_held_in(self.shoot_key)) + 1))
            self.wait_to_shoot_event.start()
class Meteorite(Component):
    length = VelocityCalculator.get_measurement(screen_length, 15);    height = VelocityCalculator.get_measurement(screen_height, 20);    left_edge_path = None;    top_edge_path = None;    time_on_path = 0;    hit_points = 5;    last_player_hit_by = 0
    def __init__(self, meteorite_path, time_for_completion, hit_points):
        super().__init__("images/meteorite.png")
        self.left_edge_path = LineSegment(Point(0, meteorite_path.start_point.x_coordinate),Point(time_for_completion, meteorite_path.end_point.x_coordinate));        self.top_edge_path = LineSegment(Point(0, meteorite_path.start_point.y_coordinate),Point(time_for_completion, meteorite_path.end_point.y_coordinate));        self.hit_points = hit_points
    def run(self):
        self.left_edge = self.left_edge_path.get_y_coordinate(VelocityCalculator.time + self.time_on_path);        self.top_edge = self.top_edge_path.get_y_coordinate(VelocityCalculator.time + self.time_on_path);         self.time_on_path = VelocityCalculator.time + self.time_on_path
class Laser(Component):
    velocity = VelocityCalculator.get_velocity(screen_height, 500);    height = VelocityCalculator.get_measurement(screen_height, 9);    length = VelocityCalculator.get_measurement(screen_length, 4);    damage = 0
    def __init__(self, left_edge, top_edge, path_to_image, size_multiplier, damage):
        Dimensions.__init__(self, left_edge, top_edge, self.length * size_multiplier, self.height * size_multiplier)
        super().__init__(path_to_image)
        self.damage = damage
    def run(self):
        self.top_edge -= VelocityCalculator.calculate_distance(self.velocity)
main_screen = NavigationScreen([MeteoriteGameScreen(1, False), MeteoriteGameScreen(2, False), MeteoriteGameScreen(2, True)], ["Single Player", "Two Player Co-op", "Two Player Versus"])
for x in range(len(main_screen.screens)):
    main_screen.screens[x].high_score = int(FileReader("high_score.txt").get_float_list("high_scores")[x])
run_game(main_screen)
open(os.getcwd() + "\\" + "high_score.txt", "w+").write(f"high_scores:{[screen.high_score for screen in game_window.screens[0].screens].__str__().replace(' ', '')}")