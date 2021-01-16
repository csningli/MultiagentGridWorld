
import sys, json, optparse, random

sys.path.append("../..")

from simulation import *

class SimpleSimulation(Simulation) :
    def __init__(self, starts : list, targets : list, obstacles : list, width : int, height : int, life : int = 1) :
        super(SimpleSimulation, self).__init__(starts = starts, targets = targets, obstacles = obstacles, width = width, height = height, life = life)
        self.tracks = [[] for i in range(len(self.world.objs))]
        self.moves = [[] for i in range(len(self.world.objs))]
        self.actions = [(0, 1), (-1, 0), (0, 1), (0, -1), (0, 0)]

    def agent_update(self, id : int, task) :
        pos = self.world.objs[id].pos
        self.tracks[id].append(pos)
        target = self.targets[id]
        move = (0, 0)
        if pos != target :
            if self.is_agent_stuck(id) :
                move = random.choice(self.actions)
            else :
                if pos[0] < target[0] :
                    move = (1, 0)
                elif pos[0] > target[0] :
                    move = (-1, 0)
                elif pos[1] < target[1] :
                    move = (0, 1)
                elif pos[1] > target[1] :
                    move = (0, -1)
        self.world.objs[id].move = move
        self.moves[id].append(move)

    def is_agent_stuck(self, id) :
        result = False
        if len(self.moves[id]) > 0 and self.moves[id][-1] != (0, 0) :
            if len(self.tracks[id]) > 1 and self.tracks[id][-1] ==  self.tracks[id][-2] :
                result = True
        return result



if __name__ == "__main__" :

    config = {
        "starts"     : [],
        "targets"    : [],
        "obstacles"  : [],
        "width"      : 20,
        "height"     : 20,
        "life"       : 1,
    }

    config = parse_arguments_for_config(config)

    sim = SimpleSimulation(**config)
    sim.run()
