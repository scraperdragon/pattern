from load import Grid, Cell, GameState, Row
from nose.tools import assert_equal


def test_grid_shape():
    x = Grid(40, 3)
    assert_equal(len(x), 3)
    assert_equal(len(x[0]), 40)
    assert_equal(type(x[2][39]), Cell)


def test_grid_cell_interactions():
    x = Grid(40, 3)
    assert_equal(x.cell(39, 2).x, 39)
    assert_equal(x.cell(39, 2).y, 2)


def test_to_moves():
    gs = GameState()
    gs.load('fixtures/solved')
    assert gs.moves == [['F', 11, 4, 1, 7],
                        ['F', 6, 14, 7, 1]]
    gs.check_vs_solved()


def test_rows():
    gs = GameState()
    gs.load('fixtures/solved')
    last_row = list(gs.rows())[-1]
    assert_equal(last_row.is_x, True)
    assert_equal(last_row.numbers, [3, 9])
    assert_equal(list(str(x) for x in last_row), list('UUUUUUFFFFFFFUU'))


def test_first_row_iteration():
    row = Row(grid=Grid(15, 3),
              is_x=True,
              offset=0,
              numbers=[1, 2, 3, 4])
    it = list(row.iterate_row())
    print it
    assert_equal(it[0], [0, 2, 5, 9])
    assert_equal(it[1], [0, 2, 5, 10])
    assert_equal(it[2], [0, 2, 5, 11])
    assert_equal(it[3], [0, 2, 6, 10])
    assert_equal(it[4], [0, 2, 6, 11])
    assert_equal(it[5], [0, 2, 7, 11])
    assert_equal(it[6], [0, 3, 6, 10])
    assert_equal(it[7], [0, 3, 6, 11])
    assert_equal(it[8], [0, 3, 7, 11])
    assert_equal(it[9], [0, 4, 7, 11])
    assert_equal(it[10], [1, 3, 6, 10])
    assert_equal(it[-1], [2, 4, 7, 11])
