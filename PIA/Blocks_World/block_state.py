# El cubo esta en la mesa?
def is_on_table(cube1):
    return cube1[1] == -1
    

# Usaremos esta clase para tener una noción en que posición esta el cubo
class BlockState(object):
    
    def __init__(self, config, n, objects, parent=None, 
                 action="Initial", cost=0, f=0, ):
        
        self.n = n
        
        self.cost = cost  # Costo g
        
        self.parent = parent
        
        self.action = action
        
        self.config = config
        '''
        config es una tupa de tuplas :
        Tuplas en config son : -1 si el cubo esta libre o el indice del cubo encima del mismo
                              y -1 si el cubo esta en la mesa o el indice del cubo debajo del mismo
        Ejemplo: (-1,3) el cubo actual esta libre y tiene debajo suyo el cubo con el indice 3
        '''
        
        self.children = []
        
        self.f = f  # Costo f
        
        self.objects = objects  # un arreglo de string que indica en que lugar 
                                # de la config se encuentra cada cubo
                                
    def expand(self):
        
        index_of_cube1 = 0
        for cube1 in self.config:
            # cube1 esta libre para mover?
            if cube1[0] == -1:
                # si cube1 no está en la tabla, mover cube1 a la tabla y 
                # crear un hijo
                if not is_on_table(cube1):
                    
                    new_config = list(map(list, self.config))
                    
                    # actualizar config
                    new_config[cube1[1]][0] = -1
                    new_config[index_of_cube1][1] = -1
                    
                    if not self.is_same_with_predecessor(new_config):
                        action = 'Move(' + self.objects[index_of_cube1] \
                            + ',' + self.objects[cube1[1]] + ',table)'
                            
                        # crear hijo
                        child = BlockState(tuple(map(tuple, new_config)), 
                                           self.n, self.objects, parent=self,
                                           action=action,
                                           cost=self.cost + 1)
                        
                        # actualizar hijo
                        self.children.append(child)
                        
                # encontrar otros cubos libres y guardar sus indices
                clear_cubes_indexes = self.find_others_free_cubes(index_of_cube1)
                
                # si hay cubos libres, mover cube1 a ese cubo y crear un hijo
                for index_of_cube2 in clear_cubes_indexes:
                    
                    new_config = list(map(list, self.config))
                    
                    # actualizar config
                    new_config[index_of_cube2][0] = index_of_cube1
                    new_config[index_of_cube1][1] = index_of_cube2
                    
                    if not is_on_table(cube1):
                        new_config[cube1[1]][0] = -1
                        
                    if not self.is_same_with_predecessor(new_config):
                        
                        if is_on_table(cube1):
                            action = 'Move(' + self.objects[index_of_cube1] \
                                + ',' + 'table' + ',' + self.objects[index_of_cube2] + ')'
                        else:
                            
                            action = 'Move(' + self.objects[index_of_cube1] \
                                    + ',' + self.objects[cube1[1]] \
                                     + ',' + self.objects[index_of_cube2] + ')'
                        # crear hijo
                        child = BlockState(tuple(map(tuple, new_config)), 
                                           self.n, self.objects, parent=self,
                                           action=action,
                                           cost=self.cost + 1)
                        # agregar a la lista de children
                        self.children.append(child)
                        
            index_of_cube1 += 1
            
    # busca y encuentra los indices de los cubos libres excepto cubo 1
    def find_others_free_cubes(self, index_of_cube1):
        clear_cubes_indexes = []
        index_of_cube2 = 0
        for cube2 in self.config:
            if cube2[0] == -1 and index_of_cube2 != index_of_cube1:
                clear_cubes_indexes.append(index_of_cube2)
            index_of_cube2 += 1
        return clear_cubes_indexes
        
    def is_same_with_predecessor(self, new_config):
        state = self
        if state.parent is not None:
            if list(map(list, state.parent.config)) == new_config:
                return True
        return False
        
    def __eq__(self, other):
        if type(other) is str:
            return False
        return self.config == tuple(map(tuple, other.config))
        
    def __lt__(self, other):
        if type(other) is str:
            return False
        return self.config < tuple(map(tuple, other.config))
        
    def __gt__(self, other):
        if type(other) is str:
            return False
        return self.config > tuple(map(tuple, other.config))