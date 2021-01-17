
import sys, os, json

from magridworld.gridworld import *
from magridworld.player import *

world = GridWorld(xlim = 2, ylim = 2,
    agents = [
        Agent(id = 0, pos = (0, -1)),
        Agent(id = 1, pos = (-1, 0)),
    ],
    obts = [
        Obstacle(id = 0, pos = (-2, 2)),
        Obstacle(id = 1, pos = (2, -2)),
    ])

if __name__ == "__main__" :
    plan = [[(0, 1), (0, 0)], [(0, 1), (1, 0)], [(0, 1), (1, 0)], [(0, 0), (1, 0)]]
    states = [world.state()]
    for moves in plan :
        world.update(moves = moves)
        states.append(world.state())

    json.dump(states, open(dirname()))
    player = Player(world = world, states = states, width = 400, height = 400, grid_size = 50)
    player.run()
