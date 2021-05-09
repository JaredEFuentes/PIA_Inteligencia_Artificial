import sys
from os import listdir
import search as s
from block_state import BlockState
from utils import parse_file, write_in_file, print_plot

"""Usage : python bw.py <method>"""

def main():
    path = "input_files/"
    execution_times = []
    nodes_problem = []
    list_files = []
    
    try:
        sm = sys.argv[1].lower()
    except IndexError:
        print("Enter valid command arguments !Usage : python bw.py <method>")
        exit(0)
    
    try:
        for file in listdir ( path ):
        #with open("input_file.pddl", 'r') as f:
            list_files.append(file.replace(".pddl", ""))
            
            objects, begin_config, goal_config = parse_file(path + file)
            
            initial_state = BlockState(begin_config, len(begin_config), objects)
            if sm == "breadth":
                state, nodes, max_depth, running_time = s.bfs_search(initial_state, goal_config)
            elif sm == "astar":
                state, nodes, max_depth, running_time = s.a_star_search(initial_state, goal_config)
            else:
                print("Enter valid command arguments !Usage : python bw.py <method>")
                exit(0)
            
            print("cost_of_path:", state.cost)
            print("nodes_expanded:", nodes)
            print("max_search_depth:", max_depth)
            print("running_time: {0:.06f}", running_time)
            
            execution_times.append(running_time)
            nodes_problem.append(nodes)
            
            moves = s.calculate_path_to_goal(state)
            valid = s.is_valid(initial_state, moves, goal_config)
            print(f'valid_solution: {valid}')
            
            write_in_file("solution_files" + file.replace(".pddl", ".txt"), moves)
            
    except EnvironmentError:
        print("File not found!")
    
    print_plot(list_files, execution_times, 'Archivo vs. Tiempos', 'Tiempo (segundos)')
    print_plot(list_files, execution_times, 'Archivo vs. Nodos', 'Cantidad de nodos')
    
if __name__ == '__main__':
    main()
