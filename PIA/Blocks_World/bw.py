import sys
import search as s
from block_state import BlockState
from utils import parse_file, write_in_file

"""Usage : python bw.py <method>"""

def main():
    try:
        sm = sys.argv[1].lower()
    except IndexError:
        print("Enter valid command arguments !Usage : python bw.py <method>")
        exit(0)
    
    try:
        with open("input_file.txt", 'r') as f:
            
            objects, begin_config, goal_config = parse_file(f)
            
            initial_state = BlockState(begin_config, len(begin_config), objects)
            if sm == "breadth":
                state, nodes, max_depth, running_time = s.bfs_search(initial_state, goal_config)
            elif sm == "astar":
                state, nodes, max_depth, running_time = s.a_star_search(initial_state, goal_config)
            else:
                print("Enter valid command arguments !Usage : python bw.py <method>")
                exit(0)
                
            moves = s.calculate_path_to_goal(state)
            write_in_file(moves)
            
            print("cost_of_path:", state.cost)
            print("nodes_expanded:", nodes)
            print("max_search_depth:", max_depth)
            print("running_time:", running_time)
            
            valid = s.is_valid(initial_state, moves, goal_config)
            if valid:
                print('valid_solution: true')
            else:
                print('valid_solution: false')
    except EnvironmentError:
        print("File not found!")
        

if __name__ == '__main__':
    main()
