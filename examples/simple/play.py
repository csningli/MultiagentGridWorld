
import sys, os, json

from magridworld.player import *
from examples.simple.main import world

if __name__ == "__main__" :
    states = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "log.json"), 'r'))
    player = Player(world = world, states = states, width = 400, height = 400, grid_size = 50)
    player.run()
