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
        self.ponto_destino_gato = glm.vec3(20, -1, 20)
        self.velocidade = 0.005  # Ajuste a velocidade conforme necessário

    def animar_gato(self):
        # Atualiza a posição do gato
        direcao = glm.normalize(self.ponto_destino_gato - self.ponto_origem_gato)
        distancia = glm.distance(self.ponto_origem_gato, self.ponto_destino_gato)
        if distancia > 0.1:  # 'epsilon' para evitar oscilação
            self.ponto_origem += direcao * self.velocidade
            self.gato.pos = (self.ponto_origem.x, self.ponto_origem.y, self.ponto_origem.z)
            self.gato.m_model = self.gato.get_model_matrix()
        

    def add_object(self, obj):
        self.objects.append(obj)

    def mover_objeto(self, obj, destino, velocidade):
    # Calcula a direção e a distância até o destino
        direcao = glm.normalize(destino - glm.vec3(obj.pos))
        distancia = glm.distance(glm.vec3(obj.pos), destino)

    # Se a distância for maior que um 'epsilon', move o objeto
        if distancia > 0.1:  # 'epsilon' para evitar oscilação quando chegar perto do destino
            nova_posicao = glm.vec3(obj.pos) + direcao * velocidade
            obj.pos = (nova_posicao.x, nova_posicao.y, nova_posicao.z)
            obj.m_model = obj.get_model_matrix()  # Atualiza a matriz do modelo
        return obj
    def load(self):
        app = self.app
        add = self.add_object
        mover = self.mover_objeto
        
        
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


        
#        cat = Cat(self.app, pos=(10, -1, 20), rot=(-90, 0, 0))
#        add(cat)
#        destino = glm.vec3(20, -1, 20)
#        cat = mover(cat, destino, 0.1)
#        self.objects[-1] = cat  # Atualiza a posição do 'Cat' na lista
        for i in range(100):
            if(i % 10 == 0):
                add(Ball(app, pos=(i, 0, i-8)))

    def render(self):
        for obj in self.objects:
            obj.render()