from load import Grid, Cell, GameState
from nose.tools import assert_equal

def test_grid_shape():
    x=Grid(40,3)
    assert_equal(len(x), 3)
    assert_equal(len(x[0]), 40)
    assert_equal(type(x[2][39]), Cell)

