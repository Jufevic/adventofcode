from pathlib import Path
from functools import cache
from collections import defaultdict, namedtuple
from math import ceil
from parse import parse

CURRENT_FILE = Path(__file__).absolute()
INPUT_FILE = Path(CURRENT_FILE.parent, 'input.txt')
DEMO_INPUT_FILE = Path(CURRENT_FILE.parent, 'demo_input.txt')
MINUTES = 24

# Parse the input and store the results in the `blueprints` list
blueprints = []
with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        (number,
        ore_robot_cost,
        clay_robot_cost,
        obsidian_robot_ore_cost,
        obsidian_robot_clay_cost,
        geode_robot_ore_cost,
        geode_robot_obsidian_cost) = parse(
            'Blueprint {:d}: Each ore robot costs {:d} ore. ' +
            'Each clay robot costs {:d} ore. ' +
            'Each obsidian robot costs {:d} ore and {:d} clay. ' +
            'Each geode robot costs {:d} ore and {:d} obsidian.',
            line
        )
        blueprint = {
            'ore': {'ore': ore_robot_cost},
            'clay': {'ore': clay_robot_cost},
            'obsidian': {
                'ore': obsidian_robot_ore_cost,
                'clay': obsidian_robot_clay_cost,
            },
            'geode': {
                'ore': geode_robot_ore_cost,
                'obsidian': geode_robot_obsidian_cost,
            }
        }
        blueprints.append(blueprint)

def quality_level(blueprint):
    """Return the quality level of the given blueprint."""
    # Compute the maximum needed amount of robot, per resource type. Needed for
    # strategy n°2.
    max_robots = defaultdict(int)
    for details in blueprint.values():
        for needed, amount in details.items():
            max_robots[needed] = max(amount, max_robots[needed])
    # There is no limit on the amount of geode robots!
    max_robots['geode'] = float('inf')

    def update_resources(robots, resources):
        """Update the quantity of resources according to the number of
        corresponding robots. Each robot collects 1 of its resource type per
        minute."""
        for resource_type in blueprint:
            resources = resources._replace(**{
                resource_type: getattr(resources, resource_type) +
                getattr(robots, resource_type)})
        return resources

    def buy_robot(robot_type, robots, resources):
        """Use the resources necessary to build the robot, then update the
        resources, then increase the robots count."""
        for needed, amount in blueprint[robot_type].items():
            resources = resources._replace(
                **{needed: getattr(resources, needed) - amount})
        resources = update_resources(robots, resources)
        robots = robots._replace(**{robot_type: getattr(robots, robot_type) + 1})
        return robots, resources

    @cache
    def max_geodes(minutes, robots, resources):
        if minutes <= 0:
            global max_so_far
            if resources.geode > max_so_far:
                max_so_far = resources.geode
            return resources.geode
        # If there is one minute remaining, buying a robot won't change the
        # final geode count, we just skip and buy nothing.
        if minutes == 1:
            resources = update_resources(robots, resources)
            return max_geodes(minutes - 1, robots, resources)

        # An optimistic heuristic on how many geodes it will be possible to
        # craft from this situation, by doing as if we could buy a robot every
        # minute (ignoring the needed resources to buy it).
        heuristic = resources.geode + minutes * ((minutes - 1) // 2 + robots.geode)
        # Strategy n°1: ignore this path if it can't give more geodes than the
        # current max.
        if heuristic < max_so_far:
            return 0

        turns_to_buy = {}

        # In how many turns will we be able to buy this robot?
        for robot_type, details in blueprint.items():
            can_buy = True
            max_turns = 0
            for needed, amount in details.items():
                if getattr(robots, needed) == 0:
                    can_buy = False
                    break
                turns = ceil((amount - getattr(resources, needed))
                             / getattr(robots, needed))
                max_turns = max(turns, max_turns)

            remaining_time = minutes - max_turns - 1
            if remaining_time < 1:
                can_buy = False

            # Strategy n°2: Don't build a robot if the current robots already
            # extract enough resources to build any robot in a single turn
            if getattr(robots, robot_type) >= max_robots[robot_type]:
                can_buy = False

            if can_buy:
                turns_to_buy[robot_type] = max_turns

        # Strategy n°3: Buy a geode robot if possible the minute before the
        # last minute
        if minutes == 2 and turns_to_buy.get('geode', float('inf')) == 0:
            robots, resources = buy_robot('geode', robots, resources)
            return max_geodes(minutes - 1, robots, resources)

        # Try to buy every possible robot and choose the best alternative
        max_result = 0
        for possible_buy, turns in turns_to_buy.items():
            new_resources = resources
            for _ in range(turns):
                new_resources = update_resources(robots, new_resources)
            new_robots, new_resources = buy_robot(possible_buy, robots, new_resources)
            remaining_time = minutes - turns - 1
            result = max_geodes(remaining_time, new_robots, new_resources)
            max_result = max(result, max_result)
        return max_result

    global max_so_far
    robots = Robots(ore=1, clay=0, obsidian=0, geode=0)
    resources = Resources(ore=0, clay=0, obsidian=0, geode=0)
    return max_geodes(MINUTES, robots, resources)

Robots = namedtuple('Robots', 'ore clay obsidian geode')
Resources = namedtuple('Resources', 'ore clay obsidian geode')
total = 0
for i, blueprint in enumerate(blueprints, start=1):
    max_so_far = 0
    quality = quality_level(blueprint)
    print(f'Blueprint {i} has quality {quality}')
    total += i * quality
print(total)