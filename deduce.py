from load import GameState  # Grid, Cell


def LogicalImpossibilityError(Exception):
    """This cell can be neither filled nor unfilled"""
    pass


def VirtualCell(dict):
    OPTIONS = [True, False]
    # True = 'F'illed, False = 'E'mpty

    for option in OPTIONS:
        self[option] = False

    def can_be(self, value):
        assert value in OPTIONS
        self[value] = True

    def is_valid(self):
        """True/False if only one possibility.
           None if both are valid.
           Raises an error if neither are."""
        if not self[True] and not self[False]:
            raise LogicalImpossibilityError
        if self[True] and not self[False]:
            return True
        if not self[True] and self[False]:
            return False
        if self[True] and self[False]:
            return None
        raise SyntaxError('Impossible!')


def make_state(filename):
    gs = GameState()
    gs.load(filename)
    return gs


def deduce(state):
    """
    For each rowcol, use sliding windows to see which cells remain permamently
    on. These should be compared to existing known cells.
    """
    for row in state.rows():
        row_solve(row)


def row_solve(row):
    """
    Given a row, attempt to solve it, at least partially.
    using *only* numbers and list(row)
    """
    print repr(row)
    for option in row.options:
        print repr(option)
        if not row.validate_possible_row(option):
            # discard if fails to match known facts
            row.options.remove(option)
            print "removed option"
        # keep record of possible values, so that at the end
        #      we can say "these cells are definately this"
        assert row.options

state = make_state('fixtures/solved')
deduce(state)
