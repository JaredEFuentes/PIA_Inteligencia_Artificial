from os import listdir
import time
import search as s
from block_state import BlockState
from utils import parse_file, write_in_file, print_plot, create_Excel, print_box

def main():
    execution_times = []
    nodes_problem = []
    list_files = []
    movements = []
    
    all_files = []
    data_for_excel = []
    
    while True:
        try:
            print("\nEscoja que tipo de algoritmos desea realizar: "
                  "\n[D]esinformados: Breadth-First Search & Depth-First Search"
                  "\n[I]nformados: A-star (3 heuristicas)")
            enter = input().lower()
            
            if enter=="d":
                busqueda = ["breadth", "depth"]
                path = "bd-input_files/"
                hoja = "Desinformed"
                break
            elif enter=="i":
                busqueda = ["heuristica_1", "heuristica_2", "ambas"]
                path = "astar-input_files/"
                hoja = "A-star"
                break
            
        except Exception:
            print("Solo ingrese una letra, porfavor")
            exit(0)
    
    
    for sm in busqueda:
        for file in listdir ( path ):
            
            # obtener datos iniciales del problema
            objects, begin_config, goal_config = parse_file(path + file)
            
            # obtener el estado inicial
            initial_state = BlockState(begin_config, len(begin_config), objects)
            
            # realizar el tipo de busqueda especificado
            if sm == "breadth":
                state, nodes, running_time = s.bfs_search(initial_state, goal_config)
            elif sm == "depth":
                state, nodes, running_time = s.dfs_search(initial_state, goal_config)
            elif enter == "i":
                state, nodes, running_time = s.a_star_search(initial_state, goal_config, sm)
            
            # es valida nuestra solución
            moves = s.calculate_path_to_goal(state)
            valid = s.is_valid(initial_state, moves, goal_config)
            
            # imprimir resultados en consola del problema
            print("\nArchivo: ", file.replace(".pddl",""))
            print("Método de Busqueda: ", sm)
            print("Se alcanzó el estado final?: ", "Si" if valid else "No")
            print("Cantidad de movimientos (Profundidad maxima recorrida): ", len(moves))
            print("Nodos expandidos: ", nodes)
            print("Tiempo de Ejecución: {0:.06f} segundos\n".format(running_time))
            
            # escribir que movimientos hacer para resolver el problema
            write_in_file("solution_files/" + file.replace(".pddl", ".txt"), moves)
            
            # datos para los plot
            list_files.append(file.replace(".pddl", "")[11:])
            movements.append(len(moves))
            nodes_problem.append(nodes)
            execution_times.append(running_time)
            
            # datos para el excel
            all_files.append(file.replace(".pddl", "")[11:])
            fila = [running_time, nodes, len(moves), sm]
            data_for_excel.append(fila)
        
        # imprimimos los tres tipos de plot para cada tipo de busqueda
        print_plot(list_files, execution_times, 'Archivo vs Tiempo', 'Tiempo (segundos)')
        print_plot(list_files, nodes_problem, 'Archivo vs Espacio', 'Cantidad de nodos')
        print_plot(list_files, movements, 'Archivo vs Movimientos', 'Cantidad de Movimientos')
        
        # re-inicializando arreglos
        list_files = []
        execution_times = []
        nodes_problem = []
        movements = []
    
    #subir datos a un excel
    columna = ["Tiempo", "Nodos", "Movimientos", "Busqueda"]
    create_Excel(data_for_excel, all_files, columna, hoja)
    
    # imprimir datos para comparar tipos de busqueda  
    print_box(hoja, "Tiempo")
    print_box(hoja, "Nodos")
    print_box(hoja, "Movimientos")
    

if __name__ == '__main__':
    main()
