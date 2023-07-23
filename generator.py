import random

class Grid:
    def __init__(self, rows, columns, bomb_count):
        self.rows = rows
        self.columns = columns
        self.grid = [[Tile(0) for _ in range(columns)] for _ in range(rows)]
        self.generate_grid(bomb_count)

    def grid_value(self, row, column):

        return self.grid[row][column].value

    def display_grid(self):
        for row in self.grid:
            row_values = [str(tile.value) for tile in row]
            print(" ".join(row_values))

    def generate_grid(self, bomb_count):
        for i in range(0, bomb_count):
            while True:
                x = random.randint(0, self.columns-1)
                y = random.randint(0, self.rows-1)
                if self.grid[y][x].value != "b":
                    self.grid[y][x] = Tile('b')
                    break
        self.calculate_adjacent_bombs()

    def calculate_adjacent_bombs(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[y][x].value == "b":
                    continue

                adjacent_bombs = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue

                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.columns and 0 <= ny < self.rows:
                            if self.grid[ny][nx].value == "b":
                                adjacent_bombs += 1

                self.grid[y][x].value = adjacent_bombs

    def check_adjacent_tiles(self, row, column):
        adjacent_tiles = {
            "north": None,
            "northeast": None,
            "east": None,
            "southeast": None,
            "south": None,
            "southwest": None,
            "west": None,
            "northwest": None,
        }

        if row != 0:
            adjacent_tiles["north"] = self.grid_value(row - 1, column)

        if column < self.columns - 1:
            adjacent_tiles["east"] = self.grid_value(row, column + 1)

        if row < self.rows - 1:
            adjacent_tiles["south"] = self.grid_value(row + 1, column)

        if column != 0:
            adjacent_tiles["west"] = self.grid_value(row, column - 1)

        if row != 0 and column < self.columns - 1:
            adjacent_tiles["northeast"] = self.grid_value(row - 1, column + 1)

        if row < self.rows - 1 and column < self.columns - 1:
            adjacent_tiles["southeast"] = self.grid_value(row + 1, column + 1)

        if row < self.rows - 1 and column != 0:
            adjacent_tiles["southwest"] = self.grid_value(row + 1, column - 1)

        if row != 0 and column != 0:
            adjacent_tiles["northwest"] = self.grid_value(row - 1, column - 1)

        return adjacent_tiles


class Tile:
    def __init__(self, value):
        self.value = value

'''
# Example usage
grid = Grid(rows=8, columns=8)
grid.generate_grid(bomb_count=10)
grid.display_grid()
'''
