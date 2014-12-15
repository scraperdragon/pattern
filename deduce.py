from load import GameState  # Grid, Cell


def poss_cells(possible, row):
    # TODO: test hard, copy to validate_possible_row
    position = 0
    output = []
    for start, length in zip(possible, row.numbers):
        while position < start:
            output.append('E')
            position = position + 1
        while position < start + length:
            output.append('F')
            position = position + 1
    while position < row.size:  # TODO off by one?
        output.append('E')
        position = position + 1

    assert len(output) == len(row)
    # print possible, row, output
    return output


def gestalt_row(row):
    gestalt = list('-' * row.size)
    for possibility in row.options:
        cells = poss_cells(possibility, row)
        for i, cell in enumerate(cells):
            if gestalt[i] == '-':
                gestalt[i] = cell  # if unknown, set to known value
            elif gestalt[i] != cell:
                gestalt[i] = 'U'   # if both options valid, set to unknown
    return gestalt


def make_state(filename):
    gs = GameState()
    gs.load(filename)
    return gs


def deduce(state):
    """
    For each rowcol, use sliding windows to see which cells remain permamently
    on. These should be compared to existing known cells.
    """
    progress = False
    while True:
        for row in state.rows():
            progress = row_solve(row) or progress
        if not progress:
            break


def row_solve(row):
    """
    Given a row, attempt to solve it, at least partially.
    using *only* numbers and list(row)
    """
    progress = False
    print repr(row)
    for option in row.options:
        print repr(option)
        if not row.validate_possible_row(option):
            # discard if fails to match known facts
            row.options.remove(option)
            print "removed option"
    g = ''.join(gestalt_row(row))
    s = str(row)
    if g != s:
        # TODO  make row values equal to gestalt row values:
        # congratulations, you've made progress!
        print "MADE PROGRESS!"
        progress = True
        row.replace(g)

    assert row.options  # we haven't destroyed all possibilities! :)
    return progress

state = make_state('fixtures/solved')
deduce(state)
