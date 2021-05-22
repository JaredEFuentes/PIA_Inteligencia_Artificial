from os import listdir
import search as s
from block_state import BlockState
from utils import parse_file, write_in_file, print_plot

def main():
    execution_times = []
    nodes_problem = []
    list_files = []
    movements = []
    
    while True:
        try:
            print("\nEscoja que tipo de busqueda desea realizar: "
                  "[B]readth/[D]epth/[A]-star")
            sm = input().lower()
            
            if sm=="b" or sm=="d":
                path = "bd-input_files/"
                break
            
            elif sm=="a":
                print("\n¿Que Heuristica desea utilizar? 1, 2 o [A]mbas")
                h = input().lower()
                if(h=="1" or h=="2" or h=="a"):
                    path = "astar-input_files/"
                    break
                    
        except Exception:
            print("Solo ingrese una letra, porfavor")
            exit(0)
    
    for file in listdir ( path ):
        
        objects, begin_config, goal_config = parse_file(path + file)
        
        initial_state = BlockState(begin_config, len(begin_config), objects)
        
        if sm == "b":
            state, nodes, running_time = s.bfs_search(initial_state, goal_config)
        elif sm == "d":
            state, nodes, running_time = s.dfs_search(initial_state, goal_config)
        elif sm == "a":
            state, nodes, running_time = s.a_star_search(initial_state, goal_config, h)
        
        moves = s.calculate_path_to_goal(state)
        valid = s.is_valid(initial_state, moves, goal_config)
        
        print("\nArchivo", file.replace(".pddl",""))
        print("Se alcanzó el estado final?: ", "Si" if valid else "No")
        print("Cantidad de movimientos (Profundidad maxima recorrida): ", len(moves))
        print("Nodos expandidos: ", nodes)
        print("Tiempo de Ejecución: {0:.06f} segundos\n".format(running_time))
        
        write_in_file("solution_files/" + file.replace(".pddl", ".txt"), moves)
        
        list_files.append(file.replace(".pddl", "")[11:])
        movements.append(len(moves))
        nodes_problem.append(nodes)
        execution_times.append(running_time)
        
    print_plot(list_files, execution_times, 'Archivo vs. Tiempo', 'Tiempo (segundos)')
    print_plot(list_files, nodes_problem, 'Archivo vs. Espacio', 'Cantidad de nodos')
    print_plot(list_files, movements, 'Archivo vs. Movimientos', 'Cantidad de Movimientos')
    
    
if __name__ == '__main__':
    main()
