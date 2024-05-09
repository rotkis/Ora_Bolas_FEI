from model import *
import glm
import numpy as np
from scipy.interpolate import interp1d


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.load_interpolacao_bola()
        self.load_interpolacao_gato()
        
        
    def load_interpolacao_bola(self):
        self.bola = Ball(self.app, pos=(1, -0.8, 0.5))  # Adicione o  aqui
        self.add_object(self.bola)  # Adicione a bola à lista de objetos
        self.velocidade_bola = 0.05  # Ajuste a velocidade conforme necessário
        self.pontos_bola_x = np.array([1, 10, 20, 30, 40, 51])
        self.pontos_bola_y = np.array([-0.8, -0.8, -0.8, -0.8, -0.8, -0.8])
        self.pontos_bola_z = np.array([2.5, 10, 20, 30, 40, 52.5])
        self.t = np.linspace(self.pontos_bola_x[0], self.pontos_bola_x[-1], num=500)
        self.interp_bola_x = interp1d(self.pontos_bola_x, self.pontos_bola_x, kind='cubic')
        self.interp_bola_y = interp1d(self.pontos_bola_x, self.pontos_bola_y, kind='cubic')
        self.interp_bola_z = interp1d(self.pontos_bola_x, self.pontos_bola_z, kind='cubic')
        self.indice_interpolacao_bola = 0

    def load_interpolacao_gato(self):
        self.gato = Cat(self.app, pos=(1, -1.5, 2), rot=(-90, 0, 0))  # Adicione o gato aqui
        self.add_object(self.gato)  # Adicione o gato à lista de objetos
        self.velocidade_gato = 0.015  # Ajuste a velocidade conforme necessário
        self.pontos_gato_x = np.array([10, 15, 20, 25])
        self.pontos_gato_y = np.array([-1.5, -1.5, -1.5, -1.5])
        self.pontos_gato_z = np.array([20, 25, 30, 35])
        self.t_gato = np.linspace(self.pontos_gato_x[0], self.pontos_gato_x[-1], num=500)
        self.interp_gato_x = interp1d(self.pontos_gato_x, self.pontos_gato_x, kind='cubic')
        self.interp_gato_y = interp1d(self.pontos_gato_x, self.pontos_gato_y, kind='cubic')
        self.interp_gato_z = interp1d(self.pontos_gato_x, self.pontos_gato_z, kind='cubic')
        self.indice_interpolacao_gato = 0

    def animar_gato(self):
        # Verifica se ainda há pontos para interpolar
        if self.indice_interpolacao_gato < len(self.t_gato):
            # Interpola os pontos
            x_interpolado_gato = self.interp_gato_x(self.t_gato[self.indice_interpolacao_gato])
            y_interpolado_gato = self.interp_gato_y(self.t_gato[self.indice_interpolacao_gato])
            z_interpolado_gato = self.interp_gato_z(self.t_gato[self.indice_interpolacao_gato])

            # Atualiza a posição do gato
            self.gato.pos = glm.vec3(x_interpolado_gato, y_interpolado_gato, z_interpolado_gato)
            self.gato.m_model = self.gato.get_model_matrix()

            # Incrementa o índice de interpolação
            self.indice_interpolacao_gato += 1

    def animar_bola(self):
        # Verifica se ainda há pontos para interpolar
        if self.indice_interpolacao_bola < len(self.t):
            # Interpola os pontos
            x_interpolado_bola = self.interp_bola_x(self.t[self.indice_interpolacao_bola])
            y_interpolado_bola = self.interp_bola_y(self.t[self.indice_interpolacao_bola])
            z_interpolado_bola = self.interp_bola_z(self.t[self.indice_interpolacao_bola])

            # Atualiza a posição da bola
            self.bola.pos = glm.vec3(x_interpolado_bola, y_interpolado_bola, z_interpolado_bola)
            self.bola.m_model = self.bola.get_model_matrix()

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
        penalti_x = 6 # campo_final_x / 5
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