
import sys, random, time, numpy, copy

class Object(object) :
    def __init__(self, id, pos) :
        self.pos = pos

    def state(self) :
        return (%s, %d, %d) % (type(self).__name__, self.pos[0], self.pos[1])

class Agent(Object) :
    def __init__(self, id, pos, target) :
        super(Agent, self).__init__(id = id, pos = pos)
        self.target = target

class Obstacle(Object) :
    def __init__(self, id, pos, target) :
        super(Obstacle, self).__init__(id = id, pos = pos)
        self.target = target

class GridWorld(object) :
    def __init__(self, xlim, ylim, agents, obts) :
        self.xlim = xlim
        self.ylim = ylim
        self.agents = agents
        self.obts = obts
        self.update_rules = [one_grid_one_obj_rule]

    def state(self) :
        return {
            "agents" : [agent.state() for agent in self.agents],
            "obts" : [obt.state() for obt in self.obts],
        }

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
