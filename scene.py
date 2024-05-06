from model import *
import glm

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.gato = Cat(app, pos=(10, -1, 20), rot=(-90, 0, 0))  # Adicione o gato aqui
        self.add_object(self.gato)  # Adicione o gato à lista de objetos
        self.ponto_origem_gato = glm.vec3(10, -1, 20)
        self.ponto_destino_gato = glm.vec3(20, -1, 30)
        self.velocidade_gato = 0.015  # Ajuste a velocidade conforme necessário
        self.bola = Ball(app, pos=(10, -1, 20))  # Adicione o gato aqui
        self.add_object(self.bola)  # Adicione a bola à lista de objetos
        self.ponto_origem_bola = glm.vec3(0, -0.27, 0)
        self.ponto_destino_bola = glm.vec3(45, -0.27, 45)
        self.velocidade_bola = 0.013  # Ajuste a velocidade conforme necessário

    def animar_bola(self):
        # Atualiza a posição da bola
        direcao = glm.normalize(self.ponto_destino_bola - self.ponto_origem_bola)
        distancia = glm.distance(self.ponto_origem_bola, self.ponto_destino_bola)
        if distancia > 0.1:  # 'epsilon' para evitar oscilação
            self.ponto_origem_bola += direcao * self.velocidade_bola
            self.bola.pos = (self.ponto_origem_bola.x, self.ponto_origem_bola.y, self.ponto_origem_bola.z)
            self.bola.m_model = self.bola.get_model_matrix()

    def animar_gato(self):
        # Atualiza a posição do gato
        direcao = glm.normalize(self.ponto_destino_gato - self.ponto_origem_gato)
        distancia = glm.distance(self.ponto_origem_gato, self.ponto_destino_gato)
        if distancia > 0.1:  # 'epsilon' para evitar oscilação
            self.ponto_origem_gato += direcao * self.velocidade_gato
            self.gato.pos = (self.ponto_origem_gato.x, self.ponto_origem_gato.y, self.ponto_origem_gato.z)
            self.gato.m_model = self.gato.get_model_matrix()
        

    def add_object(self, obj):
        self.objects.append(obj)


    def load(self):
        app = self.app
        add = self.add_object
        
        
        
        for i in range(49):
            if(i % 2 == 0):
                add(Cube(app, pos=(i, -2, -10)))
                add(Cube(app, pos=(i, -2, 80)))
            if (i % 16 == 0):
                add(Cube(app, pos=(i, -2, -8)))
                add(Cube(app, pos=(i, -2, 78)))

        for i in range(46):
            if(i % 2 == 0):
                add(Cube(app, pos=(0, -2, i-6)))
                add(Cube(app, pos=(0, -2, 76-i)))
                add(Cube(app, pos=(48, -2, i-6)))
                add(Cube(app, pos=(48, -2, 76-i)))

        for i in range(15):
            if (i% 2 == 0):
                add(Cube(app, pos=(16, -2, i-6)))
                add(Cube(app, pos=(32, -2, i-6)))
                add(Cube(app, pos=(16, -2, 76-i)))
                add(Cube(app, pos=(32, -2, 76-i)))
        
        for i in range(15):
            if (i% 2 == 0):
                add(Cube(app, pos=(16+i, -2, 8)))
                add(Cube(app, pos=(16+i, -2, 62)))

        add(Cube(app, pos=(24, -2, 4)))
        add(Cube(app, pos=(24, -2, 66)))


        for i in range(49):
            if(i % 2 == 0):
                if ( i != 0 or i != 48):
                    add(Cube(app, pos=(i, -2, 34)))
            if (i % 16 == 0):
                if ( i != 0 or i != 48):
                    add(Cube(app, pos=(i, -2, 36)))
                    add(Cube(app, pos=(i, -2, 32)))

        for i in range(9):
            if(i % 2 == 0):
                add(Cube(app, pos=(16, -2, 38+i)))
                add(Cube(app, pos=(16, -2, 30-i)))
                add(Cube(app, pos=(32, -2, 38+i)))
                add(Cube(app, pos=(32, -2, 30-i)))
        for i in range(15):
            if(i % 2 == 0):
                add(Cube(app, pos=(16+i, -2, 22)))
                add(Cube(app, pos=(16+i, -2, 46)))

        for i in range(49):
            for j in range(46):
                if(i % 2 == 0 and j % 2 ==0):
                    add(Cobe(app, pos=(i, -2, -8+j)))
                    add(Cobe(app, pos=(i, -2, 78-j)))

        # for i in range(100):
        #     if(i % 10 == 0):
        #         add(Ball(app, pos=(i, 0, i-8)))

    def render(self):
        for obj in self.objects:
            obj.render()