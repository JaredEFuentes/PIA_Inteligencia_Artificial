import time
from os import system
import seaborn as sns
import numpy as np
import pandas as pd

class Game:
    def __init__(self):
        self.game_mode = ''
        self.tablero = [['.','.','.'],
                        ['.','.','.'],
                        ['.','.','.']]
        self.turno = ''
        
        self.data_for_excel = []
    
    def draw_board(self):
        print()
        for i in range(0, 3):
            for j in range(0, 3):
                print('|{}|'.format(self.tablero[i][j]), end=" ")
            print()
        print()
    
    # Determina si el movimiento es legal
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.tablero[px][py] != '.':
            return False
        else:
            return True
    
    # Determina si se terminó el juego y quien ganó
    def is_end(self):
        # Linea Vertical
        for i in range(0, 3):
            if (self.tablero[0][i] != '.' and
                self.tablero[0][i] == self.tablero[1][i] and
                self.tablero[1][i] == self.tablero[2][i]):
                return self.tablero[0][i]
        
        # Linea Horizontal
        for i in range(0, 3):
            if (self.tablero[i][0] != '.' and
                self.tablero[i][0] == self.tablero[i][1] and
                self.tablero[i][0] == self.tablero[i][2]):
                return self.tablero[i][0]
        
        # Linea en diagonal
        if (self.tablero[0][0] != '.' and
            self.tablero[0][0] == self.tablero[1][1] and
            self.tablero[0][0] == self.tablero[2][2]):
            return self.tablero[0][0]
        
        if (self.tablero[0][2] != '.' and
            self.tablero[0][2] == self.tablero[1][1] and
            self.tablero[0][2] == self.tablero[2][0]):
            return self.tablero[0][2]
        
        # Queda algún espacio vacio?
        for i in range(0, 3):
            for j in range(0, 3):
                if (self.tablero[i][j] == '.'):
                    return None
        
        # Es un empate
        return '.'
    
    # El jugador 'O' es max, o sea, la IA
    def max(self, alpha, beta):
        # Empezamos con el peor escenario posible
        maxv = -2
        
        px = None
        py = None
        
        # Estamos en un nodo hoja?
        result = self.is_end()
        
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.tablero[i][j] == '.':
                    # Cuando topemos con un espacio en blanco, el jugador 'O'
                    # hace un movimiento y llamamos a Min para expandir el
                    # arbol de movimientos
                    self.tablero[i][j] = 'O'
                    
                    if(self.game_mode=="m"):
                        (m, min_i, min_j) = self.min(0, 0)
                    elif(self.game_mode=="p"):
                        (m, min_i, min_j) = self.min(alpha, beta)
                        
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    # Lo devolvemos a como estaba la casilla
                    self.tablero[i][j] = '.'
                        
                    if (maxv >= beta and self.game_mode=="p"):
                        return (maxv, px, py)
                    
                    if (maxv > alpha and self.game_mode=="p"):
                       alpha = maxv
                        
        return (maxv, px, py)
    
    # El jugador 'X' es min, o sea, el humano
    def min(self, alpha, beta):
        # Empezamos con el peor escenario posible
        minv = 2
        
        qx = None
        qy = None
        
        # Estamos en un nodo hoja?
        result = self.is_end()
        
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.tablero[i][j] == '.':
                    # Cuando topemos con un espacio en blanco, vamos a suponer
                    # que movimiento hara el jugador 'X' y llamamos a Max 
                    # para expandir el arbol de movimientos
                    self.tablero[i][j] = 'X'
                    
                    if(self.game_mode=="m"):
                        (m, min_i, min_j) = self.max(0, 0)
                    elif(self.game_mode=="p"):
                        (m, min_i, min_j) = self.max(alpha, beta)
                    
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.tablero[i][j] = '.'
                    
                    if (minv <= alpha and self.game_mode=="p"):
                        return (minv, qx, qy)
                    
                    if (minv < beta and self.game_mode=="p"):
                       alpha = minv
        
        return (minv, qx, qy)
    
    def play(self, gamemode, play):
        maxt = 0
        mint = 100
        fila = []
        
        self.game_mode = gamemode
        self.tablero = [['.','.','.'],
                        ['.','.','.'],
                        ['.','.','.']]
        
        # El jugador X siempre empieza primero, en este caso, el usuario
        self.turno = 'X'
        
        while True:
            self.draw_board()
            result = self.is_end()
            
            # Printing the appropriate message if the game has ended
            if  result!= None:
                if result == '.':
                    print("Es un empate!")
                else:
                    print(f'El ganador es {result}!')
                
                fila.extend((play, mint, maxt, self.game_mode))
                self.data_for_excel.append(fila)
                return
    
            # Es el turno del Jugador?
            if self.turno == 'X':
    
                while True:
                    while True:
                        try:
                            px = int(input('Inserte la coordenada X (del 1 al 3): '))
                            py = int(input('Inserte la coordenada Y (del 1 al 3): '))
                            break
                        except ValueError:
                            print('Por favor, ingrese un numero')
                        except Exception as error:
                            print(f'Unexpected error occurred {error}')
                    
                    px-=1
                    py-=1
                    if self.is_valid(px, py):
                        self.tablero[px][py] = 'X'
                        # Se pasa el turno a la IA
                        self.turno = 'O'
                        break
                    else:
                        print('Movimiento Ilegal, intentelo de nuevo.')
    
            # Es el turno de la IA?
            else:
                start = time.time()
                if(self.game_mode=="m"):
                    (m, px, py) = self.max(0, 0)
                elif(self.game_mode=="p"):
                    (m, px, py) = self.max(-2,2)
                end = time.time()
                
                execute = end - start
                
                if maxt < execute:
                    maxt = execute
                if mint > execute:
                    mint = execute
                
                print('Tiempo para movimiento: {:.6f} segundos'.format(execute))
                print(f'Movimiento a realizar: X = {px+1}, Y = {py+1}')
                
                self.tablero[px][py] = 'O'
                # Se pasa el turno al usuario
                self.turno = 'X'
    
    def create_Excel(self, rounds):
        columna = ["Round", "Min_time", "Max_time", "Gamemode"]
        df = pd.DataFrame(self.data_for_excel, index = rounds, columns = columna)
        df.to_excel('datos_rondas.xlsx', sheet_name='Hoja1')
    
    def draw_times(self):
        df = pd.read_excel('datos_rondas.xlsx', sheet_name='Hoja1')
        sns.boxplot(x="Gamemode", y="Max_time", data=df)
    
def main():
    system('cls')
    g = Game()
    i = -1
    rondas = []
    
    while True:
        
        while True:
            try:
                print('\nEscoja el modo de juego: [M]inimax/[P]runing ')
                gamemode = input().lower()
                if(gamemode=="m" or gamemode=="p"):
                    i = i+1
                    break
            except Exception:
                print("Ingrese solo una letra, por favor")
        
        rondas.append(i)
        g.play(gamemode, i)
        
        while True:
            print('Desea volver a jugar? (Y=Si, N=No): ')
            restart = input().lower()
            if(restart=='y' or restart=='n'):
                break
            else:
                print('Entrada incorrecta, por favor, vuelva a intentarlo')
        
        if restart=='n' :
            break
    
    g.create_Excel(rondas)
    g.draw_times()

if __name__ == "__main__":
    main()