
import sys, random, time, numpy, copy

class Object(object) :
    def __init__(self, id, pos) :
        self.pos = pos

    def state(self) :
        return (type(self).__name__, self.pos[0], self.pos[1])

class Agent(Object) :
    def __init__(self, id, pos, target) :
        super(Agent, self).__init__(id = id, pos = pos)
        self.target = target

class Obstacle(Object) :
    def __init__(self, id, pos) :
        super(Obstacle, self).__init__(id = id, pos = pos)

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
        attempt = [(0, 0) for i in range(len(self.agents))]
        for i, agent in enumerate(self.agents) :
            pos = (agent.pos[0] + moves[i][0], agent.pos[1] + moves[i][1])
            attempt[i] = pos if self.is_pos_valid(pos) else self.agents[i].pos
        final = [None for i in range(len(self.agents))]
        for update_rule in self.update_rules :
            attempt = update_rule(self, attempt, final)
        for i, agent in enumerate(self.agents) :
            agent.pos = attempt[i]

def one_grid_one_obj_rule(world, attempt, final) :
    forbidden_agents = []
    for i in range(- world.xlim, world.xlim + 1) :
        for j in range(- world.ylim, world.ylim + 1) :
            attempt_agents = [k for k in range(len(attempt)) if attempt[k] == (i, j)]
            if len(attempt_agents) > 1 :
                forbidden_agents += attempt_agents
    while len(forbidden_agents) > 0 :
        i = forbidden_agents.pop()
        final[i] = world.agents[i].pos
        for j, pos in enumerate(attempt) :
            if j != i and final[j] is None and pos == final[i] and j not in forbidden_agents :
                forbidden_agents.append(j)
    for i in range(len(final)) :
        if final[i] is None :
            final[i] = attempt[i]
    return final
