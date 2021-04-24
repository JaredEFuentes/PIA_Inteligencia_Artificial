from frontier_and_explored import Frontier, Explored
from block_state import BlockState
import heapq
import re
import time

PERIOD_OF_TIME = 60


def bfs_search(initial_state: BlockState, goal_config):
    """BFS search"""
    # initialize timer
    start_time = time.time()

    # initialize frontier and explored
    frontier = Frontier().queue
    frontier.append(initial_state)
    explored = Explored().set

    # frontier_configs is used just for searching and doesn't obstructs functionality
    frontier_configs = set()
    frontier_configs.add(initial_state.config)

    # initialize metrics variable
    nodes = 0

    while frontier and time.time() - start_time < PERIOD_OF_TIME:

        # pop the first state entered in frontier
        state = frontier.popleft()
        frontier_configs.remove(state.config)
        explored.add(state.config)

        # check if this state is goal state
        if state.config == goal_config:
            print("SUCCESS")
            return state, nodes, state.cost, time.time() - start_time

        # expand the state
        state.expand()
        nodes = nodes + 1

        for child in state.children:
            # check for duplicates in frontier and explored
            if child.config not in explored and child.config not in frontier_configs:
                # add child to frontier
                frontier.append(child)
                frontier_configs.add(child.config)
    print('FAILURE')
    exit()

def a_star_search(initial_state, goal_config):
    """A * search"""

    start_time = time.time()  # initialize timer

    frontier = Frontier().heap  # list of entries arranged in a heap
    entry_finder = {}  # mapping of states to entries

    explored = Explored().set  # a set of explored states

    # calculate initial's states h cost and add g cost 
    # (which is 0 so no need to add it)
    initial_state.f = h1(initial_state.config, goal_config)
    # add initial state
    add_state(initial_state, entry_finder, frontier)

    # initialize metrics variable
    nodes = 0
    max_depth = 0
    while frontier and time.time() - start_time < PERIOD_OF_TIME:
        # pop the state with the smaller cost from frontier
        state = pop_state(frontier, entry_finder)

        # check if the state has been explored
        if state.config not in explored:
            explored.add(state.config)

            # update max depth
            if max_depth < state.cost:
                max_depth = state.cost

            # check if the state is goal state
            if state.config == goal_config:
                print("SUCCESS")
                return state, nodes, max_depth, time.time() - start_time

            # expand the state
            state.expand()

            nodes = nodes + 1

            for child in state.children:
                # calculate the cost f for child
                child.f = child.cost + h2(child.config, goal_config)

                # check for duplicates in frontier
                if child.config not in entry_finder:

                    add_state(child, entry_finder, frontier)
                # if child state is already in frontier update 
                # its cost if cost is less
                elif child.f < entry_finder[child.config][0]:

                    # update the priority of an existing state
                    remove_state(child.config, entry_finder)
                    add_state(child, entry_finder, frontier)

    print('FAILURE')
    exit()

def add_state(state, entry_finder, frontier):
    """Add a new state """
    entry = [state.f, state]
    entry_finder[state.config] = entry
    heapq.heappush(frontier, entry)


def remove_state(config, entry_finder):
    """Mark an existing state as REMOVED."""
    entry = entry_finder.pop(config)
    entry[-1] = '<removed-task>'


def pop_state(frontier, entry_finder):
    """Remove and return the lowest cost state."""
    while frontier:
        state = heapq.heappop(frontier)
        if state[1] != '<removed-task>':
            del entry_finder[state[1].config]
            return state[1]

#
def h1(config, goal_config):
    """
    Heuristic 1 - this heuristic calculates the number of blocks that are 
    currently not in the correct 'position'.
    """
    cost = 0
    index = 0
    for cube in config:

        if cube[1] != goal_config[index][1]:
            cost += 1
        index += 1
    return cost

def h2(config, goal_config):
    """
    Heuristic 2 - this heuristic is similar to Heuristic 1. It calculates 
    the difference between the current state and the goal state, but looks 
    at the details of each block. If Block A in the goal state is supposed to 
    be on top of Block B and under Block C and in the current state it is 
    neither on top of B nor under C, then we add 2 to the heuristic and if 
    it is either on top of B or under C we add 1.
    """
    cost = 0
    index = 0
    for cube in config:

        if cube[0] != goal_config[index][0] and cube[1] != goal_config[1]:
            cost += 2
        elif cube[0] != goal_config[index][0] or cube[1] != goal_config[1]:
            cost += 1
        index += 1
    return cost


def calculate_path_to_goal(state):
    """calculate the path to goal"""
    moves = []
    while state.parent is not None:
        moves.append(state.action)
        state = state.parent

    moves = moves[::-1]

    return moves


def is_valid(state, moves, goal_config):
    """check if solution is valid"""
    config = list(map(list, state.config))
    objects = state.objects

    for move in moves:
        action = re.split("[(,)]", move)
        # initialize
        movedcube = objects.index(action[1])
        prevplace = action[2]
        currplace = action[3]

        # if previous place is table change the state of current place cube 
        # unclear from above and the state of moved cube to above on 
        # current place cube
        if prevplace == 'table':
            if config[objects.index(currplace)][0] == -1:
                config[movedcube][1] = objects.index(currplace)
                config[objects.index(currplace)][0] = movedcube
            else:
                return False
        # if else  current place is table change the state of previous place 
        # to clear from above
        # and the state of moved cube to on table
        elif currplace == 'table':
            if config[movedcube][0] == -1:
                config[objects.index(prevplace)][0] = -1
                config[movedcube][1] = -1
            else:
                return False
        # else change the state of current place to bellow of moved cube , 
        # the state of previous place to clear and the state of moved cube 
        # to above current place
        else:
            if config[movedcube][0] == -1 and config[objects.index(currplace)][0] == -1:
                config[objects.index(currplace)][0] = movedcube
                config[objects.index(prevplace)][0] = -1
                config[movedcube][1] = objects.index(currplace)
            else:
                return False

    return tuple(map(tuple, config)) == goal_config
