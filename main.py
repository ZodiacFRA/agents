import random
from pprint import pprint

import pygame
from pygame.locals import *

from Map import Map
from Agent import Agent

SEED = 1
GRID_SIZE = (32, 32)
FPS = 100000
TILE_SIZE = 32
MAP_ARRAY_LENGTH = GRID_SIZE[0] * GRID_SIZE[1]
WINDOW_SIZE = (GRID_SIZE[1] * TILE_SIZE, GRID_SIZE[0] * TILE_SIZE)
DRAW_GRID = False


class App(object):
    def __init__(self):
        random.seed(SEED)
        pygame.init()
        pygame.display.set_caption("Agents")
        self.display = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.fps = FPS
        # Initialize map
        self.map = Map(GRID_SIZE[0], GRID_SIZE[1])

        self.sprites = [self.load_sprite_category(id) for id in [1, 2, 4]]

        self.generation_finished = False
        self.agents = []
        self.add_new_agent()

    def launch(self):
        while not self.handle_loop():
            # print("=============", len(self.agents), "agents")
            if self.generation_finished:
                continue
            if self.agents[-1].is_active:
                self.agents[-1].do_turn(self.map)
            else:
                self.add_new_agent()
            self.display_map()

    def add_new_agent(self):
        target_size = random.randint(1, 4)
        new_pos, size = self.map.get_available_idx(target_size)
        print("tried to spawn an agent with size", target_size, "got size", size)
        if new_pos is None:
            self.generation_finished = True
            return
        agent_type_idx = random.randint(0, len(self.sprites) - 1)
        self.agents.append(Agent(self.sprites[agent_type_idx], new_pos, self.map, size))

    #########################################
    # Display functions
    def display_map(self):
        for idx in range(MAP_ARRAY_LENGTH):
            tile = self.map.get(idx)
            y, x = self.map.get_pos_from_idx(idx)
            if tile is not None:
                self.display.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
        if DRAW_GRID:
            self.draw_grid()
        pygame.display.update()

    def handle_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        self.clock.tick(self.fps)

    def draw_grid(self):
        color = (100, 100, 100)
        for y in range(0, WINDOW_SIZE[1], TILE_SIZE):
            pygame.draw.line(self.display, color, (0, y), (WINDOW_SIZE[0], y), 1)
        for x in range(0, WINDOW_SIZE[0], TILE_SIZE):
            pygame.draw.line(self.display, color, (x, 0), (x, WINDOW_SIZE[1]), 1)

    #########################################
    # Utils

    def load_sprite_category(self, id):
        return {
            "tmp": self.load_sprite(f"square_{id}"),
            "cap": self.load_sprite(f"cap_{id}"),
            "straight": self.load_sprite(f"straight_{id}"),
            "turn": self.load_sprite(f"turn_{id}"),
            "turn_sharp": self.load_sprite(f"turn_sharp_{id}"),
        }

    def load_sprite(self, sprite_name, tile_size=TILE_SIZE):
        try:
            sprite = pygame.image.load(f"""./assets/{sprite_name}.png""")
        except:
            print(f"""Error Loading ./assets/{sprite_name}.png""")
            exit()

        # Transform it to a pygame friendly format (quicker drawing)
        sprite.convert()
        sprite = pygame.transform.scale(sprite, (tile_size, tile_size))
        res = [sprite]
        for r in [-90, -180, -270]:
            res.append(pygame.transform.rotate(sprite, r))
        return res


if __name__ == "__main__":
    app = App()
    app.launch()
