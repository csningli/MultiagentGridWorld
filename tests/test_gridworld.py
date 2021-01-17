
import sys, os, time
import doctest

from magridworld.gridworld import Agent, Obstacle, GridWorld

def test_gridworld() :
    '''
    >>> test_gridworld()
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 1)
    --------------------------------------------------
    ('Agent', 1, 0)
    --------------------------------------------------
    Obstacles State:
    --------------------------------------------------
    ('Obstacle', -2, 0)
    --------------------------------------------------
    ('Obstacle', 0, -2)
    --------------------------------------------------
    Moves: [(0, 1), (1, 0)]
    --------------------------------------------------
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 2)
    --------------------------------------------------
    ('Agent', 2, 0)
    --------------------------------------------------
    '''
    world = GridWorld(xlim = 3, ylim = 3,
        agents = [
            Agent(id = 0, pos = (0, 1), target = (0, 2)),
            Agent(id = 1, pos = (1, 0), target = (2, 0)),
        ],
        obts = [
            Obstacle(id = 0, pos = (-2, 0)),
            Obstacle(id = 1, pos = (0, -2)),
        ])
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)
    print("Obstacles State:")
    print("-" * 50)
    for state in world.state()["obts"] :
        print(state)
        print("-" * 50)
    moves = [(0, 1), (1, 0)]
    print("Moves: %s" % moves)
    world.update(moves = moves)
    print("-" * 50)
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)

def test_gridworld_collision() :
    '''
    >>> test_gridworld_collision()
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 1)
    --------------------------------------------------
    ('Agent', 1, 0)
    --------------------------------------------------
    Obstacles State:
    --------------------------------------------------
    ('Obstacle', -2, 0)
    --------------------------------------------------
    ('Obstacle', 0, -2)
    --------------------------------------------------
    Moves: [(0, -1), (-1, 0)]
    --------------------------------------------------
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 1)
    --------------------------------------------------
    ('Agent', 1, 0)
    --------------------------------------------------
    '''
    world = GridWorld(xlim = 3, ylim = 3,
        agents = [
            Agent(id = 0, pos = (0, 1), target = (0, 2)),
            Agent(id = 1, pos = (1, 0), target = (2, 0)),
        ],
        obts = [
            Obstacle(id = 0, pos = (-2, 0)),
            Obstacle(id = 1, pos = (0, -2)),
        ])
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)
    print("Obstacles State:")
    print("-" * 50)
    for state in world.state()["obts"] :
        print(state)
        print("-" * 50)
    moves = [(0, -1), (-1, 0)]
    print("Moves: %s" % moves)
    world.update(moves = moves)
    print("-" * 50)
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)

def test_gridworld_alternate() :
    '''
    >>> test_gridworld_alternate()
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 1)
    --------------------------------------------------
    ('Agent', 0, 0)
    --------------------------------------------------
    Obstacles State:
    --------------------------------------------------
    ('Obstacle', -2, 0)
    --------------------------------------------------
    ('Obstacle', 0, -2)
    --------------------------------------------------
    Moves: [(0, 1), (0, 1)]
    --------------------------------------------------
    Agents State:
    --------------------------------------------------
    ('Agent', 0, 2)
    --------------------------------------------------
    ('Agent', 0, 1)
    --------------------------------------------------
    '''
    world = GridWorld(xlim = 3, ylim = 3,
        agents = [
            Agent(id = 0, pos = (0, 1), target = (0, 2)),
            Agent(id = 1, pos = (0, 0), target = (0, 1)),
        ],
        obts = [
            Obstacle(id = 0, pos = (-2, 0)),
            Obstacle(id = 1, pos = (0, -2)),
        ])
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)
    print("Obstacles State:")
    print("-" * 50)
    for state in world.state()["obts"] :
        print(state)
        print("-" * 50)
    moves = [(0, 1), (0, 1)]
    print("Moves: %s" % moves)
    world.update(moves = moves)
    print("-" * 50)
    print("Agents State:")
    print("-" * 50)
    for state in world.state()["agents"] :
        print(state)
        print("-" * 50)

if __name__ == '__main__' :
    result = doctest.testmod()
    print("-" * 50)
    print("[GridWorld Test] attempted/failed tests: %d/%d" % (result.attempted, result.failed))
