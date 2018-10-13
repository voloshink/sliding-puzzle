import queue as queue

import time
start_time = time.time()

# import resource

import sys

import math


class Frontier:
    def __init__(self, initial_state):
        self.list = []
        self.set = set()

        self.list.append(initial_state)
        self.set.add(initial_state.config)

    def add_front(self, state):
        self.list.insert(0, state)
        self.set.add(state.config)

    def add_back(self, state):
        self.list.append(state)
        self.set.add(state.config)

    def add_weighted(self, state):
        self.list.append(state)
        self.set.add(state.config)
        self.list.sort(key=lambda x: x.total_cost, reverse=True)

    def update_weight(self, state):
        for lstate in self.list:
            if lstate.config == state.config:
                lstate.total_cost = state.total_cost
                break
        self.list.sort(key=lambda x: x.total_cost, reverse=True)

    def has(self, state):
        return state.config in self.set

    def pop(self):
        state = self.list.pop()
        self.set.remove(state.config)
        return state

    def popLowest(self):
        state = self.list.pop()
        self.set.remove(state.config)
        self.list.sort(key=lambda x: x.total_cost, reverse=True)
        return state

    def len(self):
        return len(self.list)

    def is_empty(self):
        return self.len() == 0


class PuzzleState(object):

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.total_cost = -1

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = int(i / self.n)

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = int(blank_index + self.n)

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

    def isEqual(self, state):
        """comapres two nodes for equality"""

        return self.config == state.config


def write_output(state, expanded, max_depth):

    path_to_goal = []
    temp_state = state
    while temp_state.parent != None:
        path_to_goal.insert(0, temp_state.action)
        temp_state = temp_state.parent

    file = open("output.txt", "w")
    file.write("path_to_goal: {}\n".format(path_to_goal))
    file.write("cost_of_path: {}\n".format(state.cost))
    file.write("nodes_expanded: {}\n".format(expanded))
    file.write("search_depth: {}\n".format(state.cost))
    file.write("max_search_depth: {}\n".format(max_depth))
    file.write("running_time: {}\n".format(time.time() - start_time))
    # file.write("max_ram_usage: {}\n".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    file.close()

    return


def bfs_search(initial_state):
    """BFS search"""

    frontier = Frontier(initial_state)
    explored = set()

    # stats
    expanded = 0
    max_depth = 0
    while not frontier.is_empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            write_output(state, expanded, max_depth)
            break

        if len(state.children) == 0:
            children = state.expand()
            expanded += 1

        for child in children:

            if frontier.has(child):
                continue

            if child.config in explored:
                continue

            if child.cost > max_depth:
                max_depth = child.cost

            frontier.add_front(child)


def dfs_search(initial_state):
    """DFS search"""
    frontier = Frontier(initial_state)
    explored = set()

    # stats
    expanded = 0
    max_depth = 0
    while not frontier.is_empty():
        state = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            write_output(state, expanded, max_depth)
            break

        if len(state.children) == 0:
            children = reversed(state.expand())
            expanded += 1

        for child in children:

            if frontier.has(child):
                continue

            if child.config in explored:
                continue

            if child.cost > max_depth:
                max_depth = child.cost

            frontier.add_back(child)


def A_star_search(initial_state):
    """A * search"""
    frontier = Frontier(initial_state)
    explored = set()

    # stats
    expanded = 0
    max_depth = 0
    while not frontier.is_empty():
        state = frontier.popLowest()
        explored.add(state.config)

        if test_goal(state):
            write_output(state, expanded, max_depth)
            break

        if len(state.children) == 0:
            children = reversed(state.expand())
            expanded += 1

        for child in children:
            if child.config in explored:
                continue

            child.total_cost = calculate_total_cost(child)

            if frontier.has(child):
                frontier.update_weight(child)
                continue

            if child.cost > max_depth:
                max_depth = child.cost

            frontier.add_weighted(child)


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    return state.cost + calculate_manhattan_dist(state)


def calculate_manhattan_dist(state):
    """calculate the manhattan distance of a state"""
    total = 0
    for idx, tile in enumerate(state.config):
        if tile == 0:
            continue
        total += calculate_manhattan_dist_tile(tile, idx, state.n)

    return total


def calculate_manhattan_dist_tile(tile, position, n):
    """calculate the manhattan distance of a tile"""
    current_column = position % n
    current_row = int(position/n)

    goal_column = tile % n
    goal_row = int(tile/n)

    return abs(goal_column - current_column) + abs(goal_row - current_row)


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    return puzzle_state.config == (0, 1, 2, 3, 4, 5, 6, 7, 8)


def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")


if __name__ == '__main__':

    main()
