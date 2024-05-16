from model import *
import glm
import numpy as np
from scipy.interpolate import interp1d
import pygame as pg
import math


class Scene:
    
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        
        self.posicao_x = float(input("Adicione a posicao x: "))
        self.posicao_z = float(input("Adicione a posicao z: "))
        self.gato = Cat(self.app, pos=( self.posicao_x*5, -1.5, self.posicao_z*5), rot=(-90, -180, 0))
        self.ponto_origem_gato = glm.vec3( self.posicao_x*5, -1.5,  self.posicao_z*5)
        self.load_interpolacao( self.posicao_x, self.posicao_z)
        self.temp( self.posicao_x, self.posicao_z)
        self.animation_paused = True

    def check_collision(self):
        rect_bola = pg.Rect(float(self.bola.pos.x), float(self.bola.pos.z), 1, 2)
        rect_gato = pg.Rect(float(self.gato.pos.x), float(self.gato.pos.z), 1, 3)

        if rect_bola.colliderect(rect_gato):
            print(f"Collision! Ball position: ({self.bola.pos.x}, {self.bola.pos.y}, {self.bola.pos.z}), Cat position: ({self.gato.pos.x}, {self.gato.pos.y}, {self.gato.pos.z})")
            self.animation_paused = True
        
    def toggle_animation(self):
        self.animation_paused = not self.animation_paused
    
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
                


    def load_interpolacao(self,posicao_x,posicao_z):
        self.gato = Cat(self.app, pos=(posicao_x*5, -1.5, posicao_z*5), rot=(-90, -180, 0))
        self.add_object(self.gato)
        self.bola = Ball(self.app, pos=(5, -1.15, 2.5))  # Adicione o  aqui
        self.add_object(self.bola)  # Adicione a bola à lista de objetos
        with open('ball_trajectory.txt', 'r') as file:
            linhas = file.read().splitlines()
    #substituir "." por "."
        x_ball_values = [float(line.split()[1].replace(',', '.')) *5 for line in linhas[1:]]
        z_ball_values = [float(line.split()[2].replace(',', '.')) *5 for line in linhas[1:]]
        y_ball_values = [float(line.split()[3].replace(',', '.')) for line in linhas[1:]]
# Atualizar self.pontos_bola_x com os valores extraídos
        self.pontos_bola_x = np.array(x_ball_values)
        self.pontos_bola_z = np.array(z_ball_values)
        self.pontos_bola_y = np.array(y_ball_values)
        self.t = np.linspace(self.pontos_bola_x[0], self.pontos_bola_x[-1], num=500)
        self.interp_bola_x = interp1d(self.pontos_bola_x, self.pontos_bola_x, kind='cubic')
        self.interp_bola_y = interp1d(self.pontos_bola_x, self.pontos_bola_y, kind='cubic')
        self.interp_bola_z = interp1d(self.pontos_bola_x, self.pontos_bola_z, kind='cubic')
        self.indice_interpolacao_bola = 0



    def animar(self):
        velocidade_robo = 0.0901  # m/s
        acelercao_robo = 2.8  # m/s^2
        if not self.animation_paused:
        # Verifica se ainda há pontos para interpolar
            if self.indice_interpolacao_bola < len(self.t):
                fator_bola = 1.0  # Bola se move a metade da velocidade normal
                t_bola_ajustado = self.t * fator_bola
            
            # Interpola os pontos
                x_interpolado_bola = self.interp_bola_x(t_bola_ajustado)[self.indice_interpolacao_bola]
                y_interpolado_bola = self.interp_bola_y(t_bola_ajustado)[self.indice_interpolacao_bola]
                z_interpolado_bola = self.interp_bola_z(t_bola_ajustado)[self.indice_interpolacao_bola]

            # Atualiza a posição da bola
                self.bola.pos = glm.vec3(x_interpolado_bola, y_interpolado_bola, z_interpolado_bola)
                self.bola.m_model = self.bola.get_model_matrix()
   
                distance_to_ball = self.distance(self.posicao_x, self.posicao_z, self.bola.pos.x, self.bola.pos.z)
                # Definir a velocidade de rotação (em graus por quadro)
                velocidade_rotacao = 0.07

               
                direcao = glm.normalize(self.bola.pos - self.ponto_origem_gato)

                # Calcular o ângulo em graus
                angulo_alvo = math.degrees(math.atan2(direcao.z, direcao.x))

# Calcular a diferença entre o ângulo alvo e o ângulo atual
                diferenca_angulo = angulo_alvo - self.gato.rot.y

# Ajustar a diferença de ângulo para ficar entre -180 e 180
                while diferenca_angulo < -180: diferenca_angulo += 360
                while diferenca_angulo > 180: diferenca_angulo -= 360

# Calcular o ângulo de rotação com base na velocidade de rotação
                angulo_rotacao = velocidade_rotacao if diferenca_angulo > 0 else -velocidade_rotacao

# Atualizar a rotação do gato

# Atualizar a matriz de modelo
                self.gato.m_model = self.gato.get_model_matrix()
        # Calcular o tempo que o robo leva pra percorrer esse distância.
                robot_time = math.sqrt((2 * distance_to_ball) / acelercao_robo)
                # distancia = self.distance(self.ponto_origem_gato,self.bola.pos)
                if robot_time > 0.1:  # 'epsilon' para evitar oscilação
                    self.ponto_origem_gato += direcao * velocidade_robo
                    self.gato.rot.y += angulo_rotacao
                    self.gato.pos = glm.vec3(self.ponto_origem_gato.x, -1.5, self.ponto_origem_gato.z)
                    self.gato.m_model = self.gato.get_model_matrix()
                self.check_collision()
            # Incrementa o índice de interpolação
                self.indice_interpolacao_bola += 1
                
        

    def add_object(self, obj):
        self.objects.append(obj)


    def load(self):
        app = self.app
        add = self.add_object
# Definição das dimensões do campo de futebol
        campo_inicial_x = 0
        campo_inicial_z = 0
        campo_final_x = 30
        campo_final_z = 45
        meio_campo_z = campo_final_z / 2
        meio_campo_x = campo_final_x / 2
        area_x = 10 # campo_final_x / 3
        area_z = 5 # campo_final_z / 9
        penalti_z = 9 # campo_final_z / 5

# linhas do campo 
        # coluna
        for i in range(campo_final_x+1):
            add(Cube(app, pos=(i+ campo_inicial_x, -2, campo_inicial_z)))
            add(Cube(app, pos=(i+ campo_inicial_x, -2, campo_final_z)))

        # linha
        for i in range(campo_final_z +1):
            add(Cube(app, pos=(campo_inicial_x, -2, i-(campo_inicial_z))))
            add(Cube(app, pos=(campo_inicial_x, -2, (campo_final_z)-i)))
            add(Cube(app, pos=(campo_final_x, -2, i-(campo_inicial_z))))
            add(Cube(app, pos=(campo_final_x, -2, (campo_final_z)-i)))

        # coluna do meio de campo        
        for i in range(campo_final_x+1):
            add(Cube(app, pos=(i+ campo_inicial_x, -2, meio_campo_z)))

        # area do gol
        for i in range(area_z+1):
            add(Cube(app, pos=(area_x, -2, campo_inicial_z+i )))
            add(Cube(app, pos=(area_x, -2, campo_final_z-i )))
            add(Cube(app, pos=(area_x*2, -2, campo_inicial_z+i )))
            add(Cube(app, pos=(area_x*2, -2, campo_final_z-i )))
        for i in range(area_x+1):
            add(Cube(app, pos=(area_x+i, -2, campo_final_z - area_z )))
            add(Cube(app, pos=(area_x+i, -2, campo_inicial_z+ area_z )))
        
        add(Cube(app, pos=(meio_campo_x, -2, penalti_z)))
        add(Cube(app, pos=(meio_campo_x, -2, campo_final_z- penalti_z)))
        
        for x in range(campo_final_x+1):
            for z in range(campo_final_z+1):
                add(Cobe(app, pos=(x, -2, z)))
                add(Cobe(app, pos=(x, -2, campo_final_z-z)))
        
       

    def render(self):
        for obj in self.objects:
            obj.render()