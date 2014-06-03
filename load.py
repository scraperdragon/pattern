class Grid(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell(object):
    def __init__(self, x, y, state='U'):
        self.x = x
        self.y = y
        self.state = state  # default: unknown

    def set_state(self, state):
        assert state in 'FEU'
        self.state = state


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
        pass  # TODO


def main():
    gs = GameState()
    gs.load('fixtures/solved')
    print gs.moves
    print "ok"

if __name__ == "__main__":
    main()
