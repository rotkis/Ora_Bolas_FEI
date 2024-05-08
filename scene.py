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
        self.ponto_origem_bola = glm.vec3(1, -0.27, 0.5)
        self.ponto_destino_bola = glm.vec3(51   , -0.27, 10.5)
        self.velocidade_bola = 0.1  # Ajuste a velocidade conforme necessário

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
        campo_inicial_x = -1
        campo_inicial_y = -1
        campo_final_x = 8
        campo_final_y = 5
        for i in range(19): 
            add(Cube(app, pos=(i+campo_inicial_x, -2, campo_inicial_y)))
            add(Cube(app, pos=(i+campo_inicial_x, -2, campo_final_y)))
            if i % 6 == 0:
                add(Cube(app, pos=(i+campo_inicial_x, -2, campo_inicial_y+1)))
                add(Cube(app, pos=(i+campo_inicial_x, -2, campo_final_y-1)))
        for i in range(13):
            add(Cube(app, pos=(campo_inicial_x, -2, i+(campo_inicial_y-2))))
            add(Cube(app, pos=(campo_inicial_x, -2, (campo_final_y-2)-i)))
            add(Cube(app, pos=(campo_final_x, -2,i+(campo_inicial_y-2))))
            add(Cube(app, pos=(campo_final_x, -2, (campo_final_y-2)-i)))

        # for i in range(15):
        #     add(Cube(app, pos=(14, -2, i-6)))
        #     add(Cube(app, pos=(30, -2, i-6)))
        #     add(Cube(app, pos=(14, -2, 76-i)))
        #     add(Cube(app, pos=(30, -2, 76-i)))
        
        # for i in range(15):
        #     add(Cube(app, pos=(14+i, -2, 8)))
        #     add(Cube(app, pos=(14+i, -2, 62)))

        # add(Cube(app, pos=(22, -2, 4)))
        # add(Cube(app, pos=(22, -2, 66)))


        # for i in range(49):
        #     if ( i != 0 and i != 48):
        #         add(Cube(app, pos=(i-2, -2, 34)))
        #     if (i % 16 == 0):
        #         if ( i != 0 and i != 48):
        #             add(Cube(app, pos=(i-2, -2, 36)))
        #             add(Cube(app, pos=(i-2, -2, 32)))

        # for i in range(9):
        #     add(Cube(app, pos=(14, -2, 38+i)))
        #     add(Cube(app, pos=(14, -2, 30-i)))
        #     add(Cube(app, pos=(30, -2, 38+i)))
        #     add(Cube(app, pos=(30, -2, 30-i)))
        # for i in range(15):
        #     add(Cube(app, pos=(14+i, -2, 22)))
        #     add(Cube(app, pos=(14+i, -2, 46)))

        for i in range(19):
            for j in range(13):
                add(Cobe(app, pos=(i-2, -2, -8+j)))
                

        # for i in range(100):
        #     if(i % 10 == 0):
        #         add(Ball(app, pos=(i, 0, i-8)))

    def render(self):
        for obj in self.objects:
            obj.render()