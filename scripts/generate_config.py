
import sys, random, time, optparse, math, json

def generate_random_starts_and_targets(config, n : int = 1, l : int = 10) :

    # create n nodes starting randomly in l * l grids and targeting at antiposition.

    config["starts"].clear()
    config["targets"].clear()

    start_cands = [(i, j) for i in range(-l, l + 1) for j in range(-l, l + 1)]
    target_cands = [(i, j) for i in range(-l, l + 1) for j in range(-l, l + 1)]

    for i in range(n) :
        if i > (2 * l + 1) * (2 * l + 1) - 1 :
            break

        choice = random.randrange(len(start_cands))
        start = start_cands[choice]
        config["starts"].append(start)
        del(start_cands[choice])

        choice = random.randrange(len(target_cands))
        target = target_cands[choice]
        config["targets"].append(target)
        del(target_cands[choice])

    return config

if __name__ == "__main__" :

    random.seed(time.time())

    parser = optparse.OptionParser()
    parser.add_option("-n", "--number", dest="number", default = None, help="Number of agents.")
    parser.add_option("-l", "--level", dest="level", default = None, help="Number of levels.")
    parser.add_option("-m", "--method", dest="method", help="Name of the generating method.")
    parser.add_option("-o", "--output", dest="output", help="Path of the output configuration file.")
    options, args = parser.parse_args()

    func = None

    if options.method == "random" :
        func = generate_random_starts_and_targets

    config = {
        "starts"     : [],
        "targets"    : [],
        "obstacles"  : [],
        "width"      : 20,
        "height"     : 20,
        "life"       : 1,
    }

    config = func(config, n = int(options.number), l = int(options.level))

    with open(options.output, 'w') as f :
        json.dump(config, f)
