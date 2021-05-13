from os import listdir
import search as s
from block_state import BlockState
from utils import parse_file, write_in_file, print_plot

def main():
    path = "input_files/"
    execution_times = []
    nodes_problem = []
    list_files = []
    
    while True:
        try:
            print("\nEscoja que tipo de busqueda desea realizar: "
                  "[B]readth/[D]epth/[A]-star")
            sm = input().lower()
            if sm=="b" or sm=="d":
                path = "bd-input_files/"
                break
            elif sm=="a":
                path = "astar-input_files/"
                break
        except Exception:
            print("Solo ingrese una letra, porfavor")
            exit(0)
    
    #if (sm=="a"):
    for file in listdir ( path ):
    #with open(path + "probBLOCKS-30-0.pddl", 'r') as file:
        
        objects, begin_config, goal_config = parse_file(path + file)
        
        initial_state = BlockState(begin_config, len(begin_config), objects)
        if sm == "b":
            state, nodes, max_depth, running_time = s.bfs_search(initial_state, goal_config)
        elif sm == "d":
            state, nodes, max_depth, running_time = s.dfs_search(initial_state, goal_config)
        elif sm == "a":
            state, nodes, max_depth, running_time = s.a_star_search(initial_state, goal_config)
        
        print("Archivo", file.replace(".pddl",""))
        print("Costo de ruta: ", state.cost)
        print("Nodos expandidos: ", nodes)
        print("Profundidad maxima recorrida: ", max_depth)
        print("Tiempo de Ejecución: {0:.06f} segundos".format(running_time))
        
        list_files.append(file.replace(".pddl", "")[11:])
        execution_times.append(running_time)
        nodes_problem.append(nodes)
        
        moves = s.calculate_path_to_goal(state)
        write_in_file("solution_files/" + file.replace(".pddl", ".txt"), moves)
        
    print_plot(list_files, execution_times, 'Archivo vs. Tiempo', 'Tiempo (segundos)')
    print_plot(list_files, execution_times, 'Archivo vs. Espacio', 'Cantidad de nodos')
    
    
if __name__ == '__main__':
    main()
