
import sys, random, time, numpy, copy

class Object :
    def __init__(self, pos) :
        self.pos = pos

class GridWorld :
    def __init__(self, xlim, ylim, agents, obts) :
        self.xlim = xlim
        self.ylim = ylim
        self.agents = agents
        self.obts = obts
        self.update_rules = [one_grid_one_obj_rule]

    def is_pos_valid(self, pos) :
        return pos[0] >= - self.xlim and pos[0] <= self.xlim and pos[1] >= - self.ylim and pos[1] <= self.ylim

    def update(self, moves) :
        attempt = [(0, 0) for i in range(self.agents)]
        for i in range(len(self.agents)) :
            pos = (self.agents[i].pos[0] + moves[i][0], self.agents.pos[1] + moves[i][1])
            attempt[i] = pos if self.is_pos_valid(pos) else self.agents[i].pos
        for update_rule in self.update_rules :
            attempt = update_rule(self, attempt)
        for i in range(len(self.agents)) :
            self.agents[i].pos = attempt[i]

def one_grid_one_obj_rule(world, attempt) :
    final = copy.deepcopy(attempt)
    for i in range(- self.xlim, self.xlim + 1) :
        for j in range(- self.ylim, self.ylim + 1) :
            attempt_agents = [k for k in range(len(attemp)) if attempt[k] = (i, j)]
            if len(attempt_agents) > 0 :
                for k in attempt_agents :
                    final[k] = self.agents[k].pos
    return final
