import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math # matematica
from model import *


class Graphics:
    def __init__(self):
        self.posicao_x = float(input("Adicione a posicao x: "))
        self.posicao_z = float(input("Adicione a posicao z: "))
        self.coordenadas()
    def distance(self,x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    def temp(self,x_robo,y_robo):
        velocidade_robo = 2.8  # m/s
        acelercao_robo = 2.8  # m/s^2
        raio_interceptacao = 0.0943  # 9.43 em m 
        # lend o trajetoria da bola
        with open('ball_trajectory.txt', 'r') as file:
            linhas = file.read().splitlines()

    #substituir "." por "."
        for line in linhas[1:]:  
            t, x_ball, y_ball, z_ball = map(lambda val: float(val.replace(',', '.')), line.split())
    
        # Calcular a distância entre o robo e um ponto da trajetoria da bola.
            distance_to_ball = self.distance(x_robo, y_robo, x_ball, y_ball)
    
        # Calcular o tempo que o robo leva pra percorrer esse distância.
            robot_time = math.sqrt((2 * distance_to_ball) / acelercao_robo)
    
            if robot_time <= t:
                print(f"Robot intercepts the ball at t = {t} seconds, x = {x_ball} meters, y = {y_ball} meters.")
                return t
            else:
            # Calculate the new position of the robot after t seconds
                new_x_robo = x_robo + (t / 0.2) * velocidade_robo
                new_y_robo = y_robo + (t / 0.2) * velocidade_robo
        
            # Calculate the distance between the new robot position and the ball's position at time t
                new_distance_to_ball = self.distance(new_x_robo, new_y_robo, x_ball, y_ball)
        
                if new_distance_to_ball <= raio_interceptacao:
                    print(f"Robot intercepts the ball at t = {t} seconds, x = {x_ball} meters, y = {y_ball} meters.")
                    return t
        

    def coordenadas(self):
        tempo =self.temp(self.posicao_x,self.posicao_z)
        # Dados hipotéticos (substitua pelos seus dados reais)
        # Tempo de 0 a 5 segundos
        posicao_x_bola = 10 * tempo  # Exemplo: posição x da bola (função linear)
        posicao_y_bola = 5 * tempo**2  # Exemplo: posição y da bola (função quadrática)
        posicao_x_robo = 8 * tempo  # Exemplo: posição x do robô (função linear)
        posicao_y_robo = 3 * tempo**2  # Exemplo: posição y do robô (função quadrática)
        # Crie o gráfico
        plt.figure(figsize=(8, 6))
        plt.plot(tempo, posicao_x_bola, label='Posição x da bola')
        plt.plot(tempo, posicao_y_bola, label='Posição y da bola')
        plt.plot(tempo, posicao_x_robo, label='Posição x do robô')
        plt.plot(tempo, posicao_y_robo, label='Posição y do robô')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição')
        plt.title('Posição da bola e do robô em função do tempo')
        plt.legend()
        plt.grid(True)
        plt.show()

app = Graphics()


