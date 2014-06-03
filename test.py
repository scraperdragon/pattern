from load import Grid, Cell, GameState
from nose.tools import assert_equal

def test_grid_shape():
    x=Grid(40,3)
    assert_equal(len(x), 3)
    assert_equal(len(x[0]), 40)
    assert_equal(type(x[2][39]), Cell)

def test_grid_cell_interactions():
    x=Grid(40,3)
    assert_equal(x.cell(39,2).x, 39)
    assert_equal(x.cell(39,2).y, 2)

