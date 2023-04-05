import random


class Agent(object):
    def __init__(self, sprites, start_pos_idx, map, size):
        self.straightness = random.randint(0, 3)
        self.size = size
        self.is_active = False
        self.sprites = sprites
        available_directions = map.get_available_directions(start_pos_idx, self.size)
        if available_directions:
            self.is_active = True
        self.path = [(start_pos_idx, 0)]
        map.set(start_pos_idx, self.sprites["tmp"][0])

    def do_turn(self, map):
        last_pos_data = self.path[-1]
        available_directions = map.get_available_directions(last_pos_data[0], self.size)
        if not available_directions:
            self.is_active = False
            self.backtrack(map)
            return
        if (
            last_pos_data[1] in available_directions
            and random.randint(0, self.straightness) > 0
        ):
            move_direction = last_pos_data[1]
        else:
            move_direction = random.choice(available_directions)
        next_pos_idx = map.get_move_result_idx(last_pos_data[0], move_direction)
        map.set(next_pos_idx, self.sprites["tmp"][0])
        self.path.append((next_pos_idx, move_direction))

    def backtrack(self, map):
        last_tile_idx = len(self.path) - 1
        for idx, (pos_idx, direction) in enumerate(self.path):
            sprite = self.get_oriented_sprite(idx, last_tile_idx, direction)
            map.set(pos_idx, sprite, rewrite=True)

    def get_oriented_sprite(self, idx, last_tile_idx, direction):
        if idx == last_tile_idx:
            return self.sprites["cap"][(direction + 2) % 4]
        next_dir = self.path[idx + 1][1]
        if idx == 0:
            return self.sprites["cap"][next_dir]

        dir_diff = abs(direction - next_dir)
        if dir_diff == 0 or dir_diff == 2:
            return self.sprites["straight"][direction]
        else:
            sprite_type = random.choice(["turn_sharp", "turn"])
            if direction == 0:
                if next_dir == 1:
                    return self.sprites[sprite_type][3]
                if next_dir == 3:
                    return self.sprites[sprite_type][0]
            elif direction == 1:
                if next_dir == 0:
                    return self.sprites[sprite_type][1]
                if next_dir == 2:
                    return self.sprites[sprite_type][0]
            elif direction == 2:
                if next_dir == 1:
                    return self.sprites[sprite_type][2]
                if next_dir == 3:
                    return self.sprites[sprite_type][1]
            elif direction == 3:
                if next_dir == 0:
                    return self.sprites[sprite_type][2]
                if next_dir == 2:
                    return self.sprites[sprite_type][3]
