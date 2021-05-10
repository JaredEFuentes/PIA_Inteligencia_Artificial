from frontier_and_explored import Frontier, Explored
from block_state import BlockState
import heapq
import re
import time

PERIOD_OF_TIME = 60

def bfs_search(initial_state: BlockState, goal_config):
    start_time = time.time()
    
    frontier = Frontier().queue
    frontier.append(initial_state)
    explored = Explored().set
    
    # frontier_configs se usa solo para busqueda
    frontier_configs = set()
    frontier_configs.add(initial_state.config)
    
    nodes = 0
    
    while frontier and time.time() - start_time < PERIOD_OF_TIME:
        
        # sacar el primer estado que entró en frontier
        state = frontier.popleft()
        frontier_configs.remove(state.config)
        explored.add(state.config)
        
        # llegamos al estado final?
        if state.config == goal_config:
            print("SUCCESS")
            return state, nodes, state.cost, time.time() - start_time
        
        # expandir el estado
        state.expand()
        nodes = nodes + 1
        
        for child in state.children:
            # revisar por duplicados en frontier y explored
            if child.config not in explored and child.config not in frontier_configs:
                # añadir child a frontier
                frontier.append(child)
                frontier_configs.add(child.config)
    
    print('FAILURE')
    exit()

def a_star_search(initial_state, goal_config):
    start_time = time.time()
    
    frontier = Frontier().heap  # lista de entradas ordenadas en un heap
    entry_finder = {}  # mapo de estados a entradas
    
    explored = Explored().set  # un set de estados explorados
    
    # calcular la heuristica inicial
    # en este punto, el costo g es 0
    initial_state.f = h1(initial_state.config, goal_config)
    # añadir estado inicial
    add_state(initial_state, entry_finder, frontier)
    
    # inicializar variable de métricas
    nodes = 0
    max_depth = 0
    while frontier and time.time() - start_time < PERIOD_OF_TIME:
        # sacar el estado con menor costo desde frontier
        state = pop_state(frontier, entry_finder)
        
        # el estado actual ha sido explorado?
        if state.config not in explored:
            explored.add(state.config)
            
            # actualizar la profundidad maxima
            if max_depth < state.cost:
                max_depth = state.cost
            
            # hemos llegado al estado final?
            if state.config == goal_config:
                print("SUCCESS")
                return state, nodes, max_depth, time.time() - start_time
            
            # expandir el estado
            state.expand()
            
            nodes = nodes + 1
            
            for child in state.children:
                # calcular el costo f para nodo hijo
                child.f = child.cost + h1(child.config, goal_config)
                
                # revisar por duplicados en frontier
                if child.config not in entry_finder:
                    add_state(child, entry_finder, frontier)
                    
                # si un estado hijo ya está en frontier, actualiza 
                # su costo si el costo es menor
                elif child.f < entry_finder[child.config][0]:
                    
                    # actualizar la prioridad de un estado existente
                    remove_state(child.config, entry_finder)
                    add_state(child, entry_finder, frontier)
                    
    print('FAILURE')
    exit()

def add_state(state, entry_finder, frontier):
    entry = [state.f, state]
    entry_finder[state.config] = entry
    heapq.heappush(frontier, entry)
    

def remove_state(config, entry_finder):
    """Marcar un estado existente como REMOVED"""
    entry = entry_finder.pop(config)
    entry[-1] = '<removed-task>'
    

def pop_state(frontier, entry_finder):
    """Quitar y regresar el estado con el menor costo"""
    while frontier:
        state = heapq.heappop(frontier)
        if state[1] != '<removed-task>':
            del entry_finder[state[1].config]
            return state[1]
        

def h1(config, goal_config):
    """
    Heuristica 1 - Cuantos bloques no se encuentran en su posición final?
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
    Heuristica 2 - es similar a la heurisitica 1, pero busca mas detalles.
    Por ejemplo: El estado final del bloque A nos dice que dicho bloque debe
    estar encima del Bloque B y debajo del Blqoue C, pero no cumple con ninguna
    de esas condiciones, asi que agregamos 2; pero si esta encima de B o debajo
    de C, entonces solo agregamos 1.
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
    moves = []
    while state.parent is not None:
        moves.append(state.action)
        state = state.parent
        
    moves = moves[::-1]
    
    return moves
    

def is_valid(state, moves, goal_config):
    config = list(map(list, state.config))
    objects = state.objects
    
    for move in moves:
        action = re.split("[(,)]", move)
        movedcube = objects.index(action[1])
        prevplace = action[2]
        currplace = action[3]
        
        # Si el lugar previo es la tabla, cambia el estado al lugar actual
        # del cubo, sin tener claro si el cubo esta libre o no, y el estado de
        # cubo movido hacia arriba en el lugar actual del cubo
        if prevplace == 'table':
            if config[objects.index(currplace)][0] == -1:
                config[movedcube][1] = objects.index(currplace)
                config[objects.index(currplace)][0] = movedcube
            else:
                return False
        # Si el lugar actual es tabla, cambia el lugar anterior a libre desde
        # arriba y el estado de cubo movido a encima de la mesa
        elif currplace == 'table':
            if config[movedcube][0] == -1:
                config[objects.index(prevplace)][0] = -1
                config[movedcube][1] = -1
            else:
                return False
        # Si no es ninguno de los dos casos anteriores, cambia el estado del
        # lugar actual a debajo del cubo movido, el estado del lugar previo a
        # libre y el estado de cubo movido a arriba lugar actual 
        else:
            if config[movedcube][0] == -1 and config[objects.index(currplace)][0] == -1:
                config[objects.index(currplace)][0] = movedcube
                config[objects.index(prevplace)][0] = -1
                config[movedcube][1] = objects.index(currplace)
            else:
                return False
            
    return tuple(map(tuple, config)) == goal_config
