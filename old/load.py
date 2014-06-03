class Grid(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameState(object):
    def load(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        for line in lines:
            function, _, value = line.strip().split(':')
            getattr(self, function.strip())(value)
        self.apply_moves()

    def SAVEFILE(self, s):
        pass

    def VERSION(self, s):
        pass

    def GAME(self, s):
        assert s == 'Pattern'

    def PARAMS(self, s):
        self.size = [int(x) for x in s.split('x')]
        self.size_x, self.size_y = self.size
        self.grid = Grid(x,y)

    def CPARAMS(self, s):
        # TODO understand PARAM/CPARAM difference
        pass

    def DESC(self, s):
        niceheads = [h.split('.') for h in s.split('/')]
        self.heads = [niceheads[:self.size_x], niceheads[self.size_x:]]
        self.heads_x, self.heads_y = self.heads

    def NSTATES(self, s):
        pass
    
    def STATEPOS(self, s):
        pass

    def MOVE(self, s):
        # FEU: fill (black) / empty (white) / unknown (grey)
        # left, top, (0-based)
        # width, height (cells)

        if not hasattr(self, 'move'): 
            self.moves=[]
        row = [s[0]]
        row.extend(int(x) for x in s[1:].split(','))
        self.moves.append(row) 

    def applymoves(self):
        

def main():
    gs = GameState()
    gs.load('fixtures/saveex.txt')
    print gs.move
    print "ok"


if __name__ == "__main__":
    main()
