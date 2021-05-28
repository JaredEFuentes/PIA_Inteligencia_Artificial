import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_config(objects, state_in_text):
    config = list()
    
    # inicializar todos los cubos con -1
    for i in range(len(objects)):
        config.append([-1, -1])
        
    for text in state_in_text:
        tokens = re.split('[ ]', text)
        if tokens[0] == 'ON':
            index1, index2 = objects.index(tokens[1]), objects.index(tokens[2])
            config[index2][0] = index1
            config[index1][1] = index2
            
    return tuple(map(tuple, config))


def parse_file(filename):
    with open(filename, "r") as file:
        # leer objetos hasta encontrar la linea con init
        while True:
            line = file.readline()
            if "objects" in line:
                break
            
        objects = re.split("[ \n]", line)
        
        while True:
            line = file.readline()
            if ":INIT" not in line:
                objects.extend(re.split("[ \n)]", line))
            else:
                break
            
        # recortar objetos
        objects.remove("(:objects")
        while '' in objects:
            objects.remove('')
            
        while ')' in objects:
            objects.remove(')')
            
        # leer estado inicial hasta encontrar linea con goal
        init = re.split('[()\n]', line)
        
        while True:
            line = file.readline()
            if ":goal" not in line:
                init.extend(re.split('[()\n]', line))
            else:
                break
            
        # recortar init
        while '' in init:
            init.remove('')
            
        for text in init:
            if text.isspace():
                init.remove(text)
        init.remove(":INIT ")
        init.remove('HANDEMPTY')
        
        # leer estado final hasta encontrar EOF
        goal = re.split('[()\n]', line)
        
        while True:
            line = file.readline()
            if not line:
                break
            else:
                goal.extend(re.split('[()\n]', line))
                
        # recortar goal
        goal.remove(':goal ')
        goal.remove('AND ')
        
        while '' in goal:
            goal.remove('')
            
        for text in goal:
            if text.isspace():
                goal.remove(text)
                
        begin_config = create_config(objects, init)
        goal_config = create_config(objects, goal)
    
    return objects, begin_config, goal_config
    

def write_in_file(output_file, moves):
    with open(output_file, "w+") as f:
        i = 1
        for move in moves:
            f.write(str(i) + ". " + move + "\n")
            i += 1
            

def print_plot(x_plot, y_plot, title, y_name):
    # Genero la linea azul de la grafica, con los valores de x 
    # ya definidos y los tiempos de y, 'b' indica una linea azul
    plt.plot(x_plot,y_plot,'b')
    
    plt.title(title)
    plt.xlabel('Documentos')
    plt.ylabel(y_name)
    
    # Indico que quiero que se vea la cuadricula en el mapa
    plt.grid(True)
    
    # Muestro la grafica
    plt.show()

def create_Excel(data, indices, columna, hoja):
    df = pd.DataFrame(data, index = indices, columns = columna)
    df.to_excel('boxplot_block_world.xlsx', sheet_name=hoja)

def print_box(hoja, ylabel):
    df = pd.read_excel('boxplot_block_world.xlsx', sheet_name=hoja)
    sns.boxplot(x="Busqueda", y=ylabel, data=df)