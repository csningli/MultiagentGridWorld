
import sys, os, time
import doctest

from magridworld.gridworld import Object, GridWorld

def test_gridworld() :
    '''
    >>> test_gridworld()
    '''
    gridworld = GridWorld(xlim = 3, ylim = 3, agents = [Object(pos = (0, 1)), Object((pos = (1, 0)))], obts = [])

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[GridWorld Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
