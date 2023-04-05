import copy
import random


class Map(object):
    def __init__(self, row_nbr, col_nbr) -> None:
        self.row_nbr = row_nbr
        self.col_nbr = col_nbr
        map_array_len = row_nbr * col_nbr
        self.data = [None] * map_array_len
        self.available_indexes = list(range(map_array_len))

    def get_available_directions(self, idx, size):
        neighbors_idx = self.get_neighbors_idx(idx)
        return [
            direction
            for direction, idx in enumerate(neighbors_idx)
            if idx is not None and self.data[idx] is None
        ]

    def get_neighbors_idx(self, idx):
        row, col = self.get_pos_from_idx(idx)
        top_idx = idx - self.col_nbr if row > 0 else None
        right_idx = idx + 1 if col < self.col_nbr - 1 else None
        bottom_idx = idx + self.col_nbr if row < self.row_nbr - 1 else None
        left_idx = idx - 1 if col > 0 else None
        return top_idx, right_idx, bottom_idx, left_idx

    def get_move_result_idx(self, origin_pos_idx, move_direction):
        row, col = self.get_pos_from_idx(origin_pos_idx)
        if move_direction == 0:
            return origin_pos_idx - self.col_nbr if row > 0 else None
        elif move_direction == 1:
            return origin_pos_idx + 1 if col < self.col_nbr - 1 else None
        elif move_direction == 2:
            return origin_pos_idx + self.col_nbr if row < self.row_nbr - 1 else None
        elif move_direction == 3:
            return origin_pos_idx - 1 if col > 0 else None

    def get_available_idx(self, size):
        if not self.available_indexes:
            return None, -1
        while size > 0:
            # print("trying size", size)
            tmp_available_indexes = copy.copy(self.available_indexes)
            while tmp_available_indexes:
                tmp_idx = tmp_available_indexes.pop()
                random.shuffle(tmp_available_indexes)
                if self.check_available_area(tmp_idx, size):
                    return tmp_idx, size
            size -= 1
        return None, -1

    def check_available_area(self, top_left_idx, size):
        row, col = self.get_pos_from_idx(top_left_idx)
        for y in range(row, row + size):
            for x in range(col, col + size):
                tmp_idx = self.get_idx_from_pos(y, x)
                if not tmp_idx:
                    return False
                elif self.data[tmp_idx] is not None:
                    return False
        return True

    def set(self, idx, sprite, rewrite=False):
        # print("setting idx", idx)
        self.data[idx] = sprite
        if not rewrite:
            self.available_indexes.remove(idx)

    def get(self, idx):
        return self.data[idx]

    def get_pos_from_idx(self, idx):
        row = idx // self.col_nbr
        col = idx % self.col_nbr
        return row, col

    def get_idx_from_pos(self, y, x):
        if y >= self.row_nbr or x >= self.col_nbr:
            return False
        return (y * self.col_nbr) + x
