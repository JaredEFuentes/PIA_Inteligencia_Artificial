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
            print("\nEscoja que tipo de busqueda desea realizar: [B]readth/[A]-star")
            sm = input().lower()
            if(sm=="b" or sm=="a"):
                break
        except Exception:
            print("Solo ingrese una letra, porfavor")
            exit(0)
    
    try:
        for file in listdir ( path ):
        #with open("input_file.pddl", 'r') as f:
            list_files.append(file.replace(".pddl", ""))
            
            objects, begin_config, goal_config = parse_file(path + file)
            
            initial_state = BlockState(begin_config, len(begin_config), objects)
            if sm == "b":
                state, nodes, max_depth, running_time = s.bfs_search(initial_state, goal_config)
            elif sm == "a":
                state, nodes, max_depth, running_time = s.a_star_search(initial_state, goal_config)
            
            print("Costo de ruta:", state.cost)
            print("Nodos expandidos:", nodes)
            print("Profundidad maxima recorrida:", max_depth)
            print("Tiempo de Ejecución: {0:.06f}", running_time)
            
            execution_times.append(running_time)
            nodes_problem.append(nodes)
            
            moves = s.calculate_path_to_goal(state)
            valid = s.is_valid(initial_state, moves, goal_config)
            print(f'Solución valida: {valid}')
            
            write_in_file("solution_files/" + file.replace(".pddl", ".txt"), moves)
            
    except EnvironmentError:
        print("Archivo no Encontrado!")
    
    print_plot(list_files, execution_times, 'Archivo vs. Tiempo', 'Tiempo (segundos)')
    print_plot(list_files, execution_times, 'Archivo vs. Espacio', 'Cantidad de nodos')
    
if __name__ == '__main__':
    main()
