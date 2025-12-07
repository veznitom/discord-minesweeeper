import random


class MineField:
    def __init__(self, width, height, num_mines, seed=None):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        # Save seed and use a local RNG so seeding is deterministic without affecting global state
        self.seed = seed
        self._rand = random.Random(seed)
        self.field = self._generate_field()
        self._calculate_mine_counts()

    def _generate_field(self):

        # Create an empty field
        field = [['0' for _ in range(self.width)] for _ in range(self.height)]

        # Place mines randomly using the local RNG
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = self._rand.randint(0, self.width - 1)
            y = self._rand.randint(0, self.height - 1)
            if field[y][x] != '*':
                field[y][x] = '*'
                mines_placed += 1

        return field

    def _calculate_mine_counts(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] == '*':
                    continue
                mine_count = 0
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        if self.field[ny][nx] == '*':
                            mine_count += 1
                self.field[y][x] = str(mine_count) if mine_count > 0 else '0'

    def display_field(self):
        for row in self.field:
            print(' '.join(row))
        print(f"Size: {self.width} x {self.height} Mines: {self.num_mines}\n")