import logging
logging.basicConfig(level=logging.INFO)

class OutOfBoundsError(IndexError):
    pass

class Row(list):
    def __init__(self, **kwargs):
        self.grid = kwargs['grid']
        assert isinstance(self.grid, Grid)

        self.is_x = kwargs['is_x']
        assert isinstance(self.is_x, bool)

        if self.is_x:
            self.size = self.grid.x
        else:
            self.size = self.grid.y

        self.offset = kwargs['offset']
        assert isinstance(self.offset, int)

        for i in range(self.size):
            if self.is_x:
                self.append(self.grid.cell(i, self.offset))
            else:
                self.append(self.grid.cell(self.offset, i))

        self.numbers = kwargs['numbers']
        assert isinstance(self.numbers, list)


    def __repr__(self):
        row = ''.join(str(x) for x in self)
        return "{!r}: {!r}".format(self.numbers, row)

class Grid(list):
    def __init__(self, x_size, y_size):
        self.x = x_size
        self.y = y_size
        for y in range(y_size):
            row = list()
            for x in range(x_size):
                row.append(Cell(x, y))

            self.append(row)

    def cell(self, x, y):
        try:
            return self[y][x]
        except IndexError:
            raise OutOfBoundsError('cell({!r}, {!r}) asked for, '\
                'but grid is ({!r}, {!r})'.format(x, y, self.x, self.y))

    def pprint(self):
        def row_text(row):
            return ''.join(cell.state for cell in row)
        print '\n'.join(row_text(row) for row in self)

    def as_solution(self):
        def row_text(row):
            return ''.join(cell.state for cell in row)
        concat = ''.join(row_text(row) for row in self)
        for pair in ['F1', 'E0', 'U9']:
            concat = concat.replace(pair[0], pair[1])
        return concat


class Cell(object):
    def __init__(self, x, y, state='U'):
        self.x = x
        self.y = y
        self.colour(state)  # default: unknown

    def __repr__(self):
        return self.state

    def colour(self, state):
        assert state in 'FEU'
        self.state = state


class GameState(object):
    def pprint(self):
        return self.grid.pprint()

    def load(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        for line in lines:
            function, _, value = line.strip().split(':')
            getattr(self, function.strip())(value)
        self.apply_moves()

    def rows(self):
        for x in range(self.grid.x):
            yield Row(grid=self.grid,
                      is_x=False,
                      offset=x,
                      numbers=self.heads_x[x])
        for y in range(self.grid.y):
            yield Row(grid=self.grid,
                      is_x=True,
                      offset=y,
                      numbers=self.heads_y[y])

    def dont_care(*args, **kwargs):
        pass

    SAVEFILE = VERSION = SEED = AUXINFO = dont_care
    NSTATES = STATEPOS = CPARAMS = dont_care
    # TODO - how is CPARAMS different to PARAMS?

    def SOLVE(self, s):
        assert s[0] == 'S'
        self.solved = s[1:]  ## just record

    def GAME(self, s):
        assert s == 'Pattern'

    def PARAMS(self, s):
        self.size = [int(x) for x in s.split('x')]
        self.size_x, self.size_y = self.size
        self.grid = Grid(*self.size)

    def DESC(self, s):
        def intify(l):
            return [int(i) for i in l]
        niceheads = [h.split('.') for h in s.split('/')]
        self.heads = [niceheads[:self.size_x], niceheads[self.size_x:]]
        self.raw_heads_x, self.raw_heads_y = self.heads
        self.heads_x = map(intify, self.raw_heads_x)
        self.heads_y = map(intify, self.raw_heads_y)

    def MOVE(self, s):
        # FEU: fill (black) / empty (white) / unknown (grey)
        # left, top, (0-based)
        # width, height (cells)
        logging.info("MOVE {!r}".format(s))
        if not hasattr(self, 'moves'):
            self.moves = []
        row = [s[0]]
        row.extend(int(x) for x in s[1:].split(','))
        self.moves.append(row)

    def apply_moves(self):
        for move in self.moves:
            feu, left, top, width, height = move
            for x in range(left, left + width):
                for y in range(top, top + height):
                    self.grid.cell(x, y).colour(feu)

    def check_vs_solved(self):
        if not hasattr(self, 'solved'):
            raise RuntimeError("No solution available.")
        grid_sol = self.grid.as_solution()
        assert len(self.solved) == len(grid_sol)
        for pair in zip(list(self.solved), list(grid_sol)):
            assert pair[0] == pair[1] or \
                   pair[1] == '9', \
                   "Expected {}, had {} at {}".format(pair[0], pair[1], -1)


def main():
    gs = GameState()
    gs.load('fixtures/solved')
    gs.pprint()
    gs.check_vs_solved()

    print gs.heads

if __name__ == "__main__":
    main()
