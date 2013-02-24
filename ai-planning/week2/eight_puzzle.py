import sys
from Queue import PriorityQueue
from copy import copy
import time

NAV_MAPS = {
         "right":[1, 1, 0, 1, 1, 0, 1, 1, 0],
         "left":[0, 1, 1, 0, 1, 1, 0, 1, 1],
         "up":[0, 0, 0, 1, 1, 1, 1, 1, 1],
         "down":[1, 1, 1, 1, 1, 1, 0, 0, 0]}

MOVES = {         
         "right":1,
         "left":-1,
         "up":-3,
         "down":3}

def value_at(value, state):
    return [idx for idx in range(9) if state[idx] == value][0]

def misplaced_blocks(state, goal):
    return len([idx for idx in range(9) if (state[idx] != goal[idx])])

def heuristic(state, goal):
    return misplaced_blocks(state, goal);

def is_goal(state, goal):
    return (misplaced_blocks(state, goal) == 0)

def new_state(state, blank_at, nav_map_key):
    new_state = copy(state)
    target_idx = blank_at + MOVES.get(nav_map_key)
    new_state[blank_at] = state[target_idx]
    new_state[target_idx] = 0
    return new_state

def is_move_allowed(blank_at, nav_map_key):
    return (NAV_MAPS.get(nav_map_key)[blank_at] == 1);

def expand(state):
    successors = []
    blank_at = value_at(0, state)
    for nav_map_key in NAV_MAPS:
        if (is_move_allowed(blank_at, nav_map_key)):
            successors.append(new_state(state, blank_at, nav_map_key))
    return successors

def hash_state(list):
    hash = ''
    for idx in range(9):
        hash += str(list[idx])
    return hash

def solve(state, goal):
    
    initial_state = copy(state)
    
    fringe = PriorityQueue()
    visited = 0
    
    g = 0
    h = heuristic(state, goal)
    f = h + g
    fringe.put((f, (state, h, g)))
    
    hash = hash_state(state)
    known_nodes = {}
    known_nodes[hash] = (None, state)

    while True:
        
        if fringe.empty():
            return (False, g, visited, None)
        
        (f, (state, h, g)) = fringe.get()
        visited += 1
        
        if (DEBUG): 
            print '> state is: %s with f(x)=%d, h(x)=%d and g(x)=%d' % (state, f, h, g)
        
        #path.append(state)
        if (is_goal(state, goal)):
            path = []
            s = state
            finished = False
            while not finished:
                if (s == initial_state): 
                    finished = True
                    continue
                path.append(s)
                (p, t) = known_nodes[hash_state(s)]
                s = p
            path.reverse()
            return (True, g, visited, path)

        if (DEBUG): print '  > expanding current state...'
        
        g_prime = g + 1 
        for successor in expand(state):
            
            hash = hash_state(successor)
            if (known_nodes.has_key(hash)):
                if (DEBUG): 
                    print '\t> discarding state: %s...' % (successor)
                continue
            
            h_prime = heuristic(successor, goal)
            f_prime = h_prime + g_prime
            
            if (DEBUG): 
                print '\t> state is: %s with f(x)=%d, h(x)=%d and g(x)=%d' % (successor, f_prime, h_prime, g_prime)

            fringe.put((f_prime, (successor, h_prime, g_prime)))
            known_nodes[hash] = (state, successor)

    return 

def usage():
    print '--------------------------------------------------------------------------------'
    print 'Eigth puzzle A* star search and misplaced tiles heuristic'
    print '--------------------------------------------------------------------------------'
    print 'usage:'
    print 'initial_state\tthe initial 3x3 puzzle state as a comma separated string'
    print 'goal_state   \tthe 3x3 puzzle goal state as a comma separated string'
    print '[debug]      \tprint progress messages (\'on/off\' - default is \'off\')'
    print '--------------------------------------------------------------------------------\n'
    return

def main():

    usage()
    
    if len(sys.argv) != 3:
        return

    state_str = sys.argv[1]
    goal_str = sys.argv[2]
    
    global DEBUG
    DEBUG = True if (len(sys.argv) == 4 and sys.argv[3] == 'on') else False
    
    state = map(int, state_str.split(','))
    if len(state) != 9:
        print 'invalid initial state'
        return

    goal = map(int, goal_str.split(','))
    if len(goal) != 9:
        print 'invalid goal state'
        return

    print 'initial puzzle state is %s' % state
    print 'puzzle goal is %s' % goal

    # TODO: check solvability

    start = time.clock()
    (found, depth, visited, path) = solve(state, goal)
    end = time.clock() - start

    if (found):
        print '\ngoal can be reached in %d steps' %  depth
        print '> this path was found in %0.2f seconds after visiting %d nodes' % (end, visited)
        print '> path to goal is:'
        for idx in range(depth):
            print '  > (%d) = %s' % (idx + 1, path[idx])
    else:
        print '\ngoal could not be reached'
    return 

if __name__ == "__main__":
    main()
