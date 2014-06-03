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
        return self[x][y]

class Cell(object):
    def __init__(self, x, y, state='U'):
        self.x = x
        self.y = y
        self.colour(state)  # default: unknown

    def colour(self, state):
        assert state in 'FEU'
        self.colour = state


class GameState(object):
    def load(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        for line in lines:
            function, _, value = line.strip().split(':')
            getattr(self, function.strip())(value)
        self.apply_moves()

    def dont_care(*args, **kwargs):
        pass

    SAVEFILE = VERSION = SEED = AUXINFO = SOLVE = dont_care
    NSTATES = STATEPOS = CPARAMS = dont_care
    # TODO - how is CPARAMS different to PARAMS?

    def GAME(self, s):
        assert s == 'Pattern'

    def PARAMS(self, s):
        self.size = [int(x) for x in s.split('x')]
        self.size_x, self.size_y = self.size
        self.grid = Grid(*self.size)

    def DESC(self, s):
        niceheads = [h.split('.') for h in s.split('/')]
        self.heads = [niceheads[:self.size_x], niceheads[self.size_x:]]
        self.heads_x, self.heads_y = self.heads

    def MOVE(self, s):
        # FEU: fill (black) / empty (white) / unknown (grey)
        # left, top, (0-based)
        # width, height (cells)

        if not hasattr(self, 'move'):
            self.moves = []
        row = [s[0]]
        row.extend(int(x) for x in s[1:].split(','))
        self.moves.append(row)

    def apply_moves(self):
        for move in self.moves:
            feu, left, top, width, height = move
            for x in range(left, left + width):
                for y in range(top, top + height):
                    self.grid.cell(x,y).colour(feu)


def main():
    gs = GameState()
    gs.load('fixtures/solved')
    print gs.moves
    print "ok"

if __name__ == "__main__":
    main()
