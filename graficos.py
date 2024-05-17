import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import math

class Graphics:
    def __init__(self):
        self.posicao_x_robo = []
        self.posicao_z_robo = []
        self.posicao_x_bola = []
        self.posicao_z_bola = []
        self.trajetoria_robo = []
        self.trajetoria_bola = []
        self.velocidades_robo = []
        self.velocidades_bola = []
        self.aceleracao_robo = []
        self.aceleracao_bola = []
        self.distancias = []
        self.posicao_x = float(input("Adicione a posicao x: "))
        self.posicao_z = float(input("Adicione a posicao z: "))
        self.tempo = []
        self.temp(self.posicao_x, self.posicao_z)
        self.calcula_velocidade(self.trajetoria_robo, self.trajetoria_bola)
        self.run()


    def run(self):
        self.coordenadas()
        self.componente_v()
        self.componete_a()
        self.distancia()

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def calcula_aceleracao(self, velocidades_robo, velocidades_bola):
        for i in range(1, len(velocidades_robo)):
            ax = (velocidades_robo[i][0] - velocidades_robo[i-1][0]) / 0.02
            ay = (velocidades_robo[i][1] - velocidades_robo[i-1][1]) / 0.02
            if ax > 2.8 and ay > 2.8:
                ax = 2.8
                ay= 2.8
            self.aceleracao_robo.append([ax, ay])

        for i in range(1, len(velocidades_bola)):
            ax = (velocidades_bola[i][0] - velocidades_bola[i-1][0]) / 0.02
            ay = (velocidades_bola[i][1] - velocidades_bola[i-1][1]) / 0.02
            self.aceleracao_bola.append([ax, ay])

    def calcula_velocidade(self, trajetoria_robo, trajetoria_bola):
        for i in range(1, len(trajetoria_robo)):
            vx = (trajetoria_robo[i][0] - trajetoria_robo[i-1][0]) / 0.02
            vy = (trajetoria_robo[i][1] - trajetoria_robo[i-1][1]) / 0.02
            if vx > 2.8 and vy > 2.8:
                vx = 2.8
                vy= 2.8
            self.velocidades_robo.append([vx, vy])

        for i in range(1, len(trajetoria_bola)):
            vx = (trajetoria_bola[i][0] - trajetoria_bola[i-1][0]) / 0.02
            vy = (trajetoria_bola[i][1] - trajetoria_bola[i-1][1]) / 0.02
            self.velocidades_bola.append([vx, vy])

        self.calcula_aceleracao(self.velocidades_robo, self.velocidades_bola)

    def temp(self, x_robo, y_robo):
        velocidade_robo = 2.8  # m/s
        raio_interceptacao = 0.0943  # 9.43 em mm
        new_x_robo = x_robo
        new_y_robo = y_robo
        i = 0

        # Lendo a trajetória da bola
        with open('ball_trajectory.txt', 'r') as file:
            linhas = file.read().splitlines()

        for line in linhas[1:]:
            t, x_ball, y_ball, z_ball = map(lambda val: float(val.replace(',', '.')), line.split())

            direcao = [x_ball - new_x_robo, y_ball - new_y_robo]
            norma = math.sqrt(direcao[0] ** 2 + direcao[1] ** 2)
            direcao = [direcao[0] / norma, direcao[1] / norma]

            new_x_robo += direcao[0] * velocidade_robo * 0.02
            new_y_robo += direcao[1] * velocidade_robo * 0.02

            self.trajetoria_robo.append([new_x_robo, new_y_robo])
            self.trajetoria_bola.append([x_ball, y_ball])
            self.tempo.append(i * 0.02)
            self.posicao_x_robo.append(new_x_robo)
            self.posicao_z_robo.append(new_y_robo)
            self.posicao_x_bola.append(x_ball)
            self.posicao_z_bola.append(y_ball)
            self.distancias.append(self.distance(new_x_robo, new_y_robo, x_ball, y_ball))

            if self.distance(new_x_robo, new_y_robo, x_ball, y_ball) <= raio_interceptacao:
                print(f"O robô alcançou a bola no tempo {i * 0.02:.2f}s, na posição [{new_x_robo:.3f}, {new_y_robo:.3f}]")
                break
            i += 1

    def coordenadas(self):
        plt.figure(figsize=(10, 12))
        plt.plot(self.tempo, self.posicao_x_bola, label='Posição x da bola')
        plt.plot(self.tempo, self.posicao_z_bola, label='Posição y da bola')
        plt.plot(self.tempo, self.posicao_x_robo, label='Posição x do robô')
        plt.plot(self.tempo, self.posicao_z_robo, label='Posição y do robô')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição')
        plt.title('Posição da bola e do robô em função do tempo')
        plt.legend()
        plt.grid(True)
        plt.show()

    def componente_v(self):
        plt.figure(figsize=(10, 12))
        plt.plot(self.tempo[1:], [vel[0] for vel in self.velocidades_robo], label='Robô vx')
        plt.plot(self.tempo[1:], [vel[1] for vel in self.velocidades_robo], label='Robô vy')
        plt.plot(self.tempo[1:], [vel[0] for vel in self.velocidades_bola], label='Bola vx')
        plt.plot(self.tempo[1:], [vel[1] for vel in self.velocidades_bola], label='Bola vy')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Velocidade')
        plt.title('Componentes da velocidade da bola e do robô')
        plt.legend()
        plt.grid(True)
        plt.show()

    def componete_a(self):
        plt.figure(figsize=(10, 12))
        plt.plot(self.tempo[2:], [acc[0] for acc in self.aceleracao_robo], label='Robô ax')
        plt.plot(self.tempo[2:], [acc[1] for acc in self.aceleracao_robo], label='Robô ay')
        plt.plot(self.tempo[2:], [acc[0] for acc in self.aceleracao_bola], label='Bola ax')
        plt.plot(self.tempo[2:], [acc[1] for acc in self.aceleracao_bola], label='Bola ay')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Aceleração')
        plt.title('Componentes da aceleração da bola e do robô')
        plt.legend()
        plt.grid(True)
        plt.show()

    def distancia(self):
        plt.figure(figsize=(10, 12))
        plt.plot(self.tempo, self.distancias, label='Distância')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Distância')
        plt.title('Distância entre a bola e o robô')
        plt.legend()
        plt.grid(True)
        plt.show()

app = Graphics()
