
import sys, random, time, datetime, optparse, json, numpy, pycos, copy

from gridworld import *

class Simulation :
    def __init__(self, starts : list, targets : list, obstacles : list, width : int, height :int, life : int) :
        self.width = width
        self.height = height
        self.life = life
        self.targets = []
        self.observes = []
        self.time = 0
        obts = [Dot(pos = pos) for pos in obstacles]
        objs = [Dot(pos = pos) for pos in starts]
        self.world = GridWorld(width = self.width, height = self.height, objs = objs, obts = obts)
        for pos in targets :
            self.targets.append(pos)
        self.data = []

    def record(self) :
        record = [obj.pos for obj in self.world.objs]
        self.data.append(record)

    def monitor_proc(self, task = None) :
        print("[%f] Monitor starts." % time.time())
        task.set_daemon()
        self.record()
        clock = 0
        while clock < self.life - 0.000001 :
            self.world.update()
            self.record()
            self.monitor_update(task = task)
            clock = yield clock + 1
        print("[%f] Monitor ends." % time.time())
        self.save()

    def sensor_proc(self, id : int, task = None) :
        clock = 0
        while clock < self.life - 0.000001 :
            self.sensor_update(id = id, task = task)
            clock = yield clock + 1

    def agent_proc(self, id : int, task = None) :
        pos = self.world.objs[id].pos
        target = self.targets[id]
        clock = 0
        while clock < self.life - 0.000001 and pos != target :
            self.agent_update(id = id, task = task)
            clock = yield clock + 1

    def monitor_update(self, task) :
        # print("[%f] Monitor updates." % time.time())
        pass

    def sensor_update(self, id : int, task) :
        # print("[%f] Sensor  updates." % time.time()
        pass

    def agent_update(self, id : int, task) :
        # print("[%f] Agent %d updates." % (time.time(), id))
        pass

    def run(self) :
        self.time = 0.0
        for i in range(len(self.world.obts)) :
            pycos.Task(self.sensor_proc, id = i)
        for i in range(len(self.world.objs)) :
            pycos.Task(self.agent_proc, id = i)
        pycos.Task(self.monitor_proc)

    def save(self, filename : str = None) :
        if filename is None :
            timelabel = datetime.datetime.now().strftime('%Y%m%d%H%M%S_%f')
            classname = type(self).__name__
            prefix = classname[:classname.find("Simulation")].lower()
            filename = f"{prefix}{'-' * int(len(prefix) > 0)}{timelabel}.log"

        config = {
            "targets"   : [target for target in self.targets],
            "obstacles" : [obt.pos for obt in self.world.obts],
            "width"     : self.width,
            "height"    : self.height,
            "life"      : self.life,
            "data"      : self.data,
        }

        with open(filename, 'w') as f :
            json.dump(config, f)


def parse_arguments_for_config(config : dict) :
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest = "config", help = "Path to the configuration file.")
    options, args = parser.parse_args()

    with open(options.config, 'r') as f :
        data = json.load(f)
        for key in ["starts", "targets", "obstacles", "width", "height", "life"] :
            config[key] = data.get(key, None)

    return config
