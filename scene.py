import math

import glm
import numpy as np
from scipy.interpolate import CubicSpline

from model import Cat, Ball, StaticMesh

# Plotas do campo em unidades de cena
FLOOR_TEX, FIELD_TEX = 1, 0
CAT_SCALE = 2.0


class Scene:
    def __init__(self, app, posicao_x=0.0, posicao_z=0.0):
        self.app = app
        self.objects = []

        # Campo estático: 2 draw calls (piso + linhas)
        self.add_object(StaticMesh(app, "floor", FLOOR_TEX))
        self.add_object(StaticMesh(app, "field", FIELD_TEX))

        self.posicao_x = posicao_x
        self.posicao_z = posicao_z

        self.cat = Cat(
            app,
            pos=(posicao_x * 5, -1.5 + CAT_SCALE / 2, posicao_z * 5),
            rot=(-90, -180, 0),
        )
        self.ponto_origem_gato = glm.vec3(self.cat.pos)
        self.add_object(self.cat)

        self.ball = Ball(app, pos=(5, -1.15, 2.5))
        self.add_object(self.ball)

        self.load_interpolacao()
        self.animation_paused = True
        self.interceptado = False

    # ------------------------------------------------------------------ #
    #  Trajetória e interpolação da bola
    # ------------------------------------------------------------------ #
    def load_interpolacao(self):
        from pathlib import Path

        path = Path(__file__).resolve().parent / "ball_trajectory.txt"
        data = np.genfromtxt(
            path,
            converters={i: lambda s: float(s.replace(",", ".")) for i in range(4)},
        )
        data = data[1:]  # descarta cabeçalho (quando houver números no cabeçalho já ok)

        # Coordenadas de cena: plano XZ * 5, altura Y em metros
        self.pontos_bola_x = data[:, 1] * 5.0
        self.pontos_bola_z = data[:, 2] * 5.0
        self.pontos_bola_y = data[:, 3]

        self.t_interp = np.linspace(
            self.pontos_bola_x[0], self.pontos_bola_x[-1], num=500
        )
        cs_x = CubicSpline(self.pontos_bola_x, self.pontos_bola_x)
        cs_y = CubicSpline(self.pontos_bola_x, self.pontos_bola_y)
        cs_z = CubicSpline(self.pontos_bola_x, self.pontos_bola_z)
        # Interpola 1x na inicialização; o frame só indexa o array pronto.
        self.bola_x_t = cs_x(self.t_interp)
        self.bola_y_t = cs_y(self.t_interp)
        self.bola_z_t = cs_z(self.t_interp)
        self.indice_interpolacao_bola = 0
        # Tempo (s) de cada passo da animação: a trajetória toda (len(data) linhas
        # x 0.02s) é percorrida em len(t_interp) passos.
        self.dt_passo = 0.02 * len(data) / len(self.t_interp)

    # ------------------------------------------------------------------ #
    #  Animação
    # ------------------------------------------------------------------ #
    @staticmethod
    def distance(x1, y1, x2, y2) -> float:
        return math.hypot(x2 - x1, y2 - y1)

    def animar(self):
        velocidade_robo = 0.0901  # unidades de cena / frame
        if self.animation_paused or self.interceptado:
            return

        i = self.indice_interpolacao_bola
        if i >= len(self.t_interp):
            self.animation_paused = True
            return

        self.ball.pos = glm.vec3(self.bola_x_t[i], self.bola_y_t[i], self.bola_z_t[i])
        self.ball.m_model = self.ball.get_model_matrix()
        self.indice_interpolacao_bola += 1

        distancia_ate_bola = self.distance(
            self.cat.pos.x, self.cat.pos.z, self.ball.pos.x, self.ball.pos.z
        )
        if distancia_ate_bola <= 1.0:
            dt = i * self.dt_passo
            print(
                f"O robô alcançou a bola no tempo {dt:.2f}s, "
                f"em ({self.ball.pos.x:.2f}, {self.ball.pos.z:.2f})"
            )
            self.interceptado = True
            self.animation_paused = True
            return

        # Direção ao alvo
        direcao = glm.normalize(self.ball.pos - self.ponto_origem_gato)

        # Rotação suave do robô em direção à bola
        angulo_alvo = math.degrees(math.atan2(direcao.z, direcao.x))
        diferenca_angulo = (
            angulo_alvo - math.degrees(self.cat.rot.y) + 180
        ) % 360 - 180
        velocidade_rotacao = 0.07
        self.cat.rot.y += glm.radians(
            velocidade_rotacao if diferenca_angulo > 0 else -velocidade_rotacao
        )

        # Movimento em direção à bola
        self.ponto_origem_gato += direcao * velocidade_robo
        self.cat.pos = glm.vec3(
            self.ponto_origem_gato.x, self.cat.pos.y, self.ponto_origem_gato.z
        )
        self.cat.m_model = self.cat.get_model_matrix()

    def toggle_animation(self):
        self.animation_paused = not self.animation_paused

    # ------------------------------------------------------------------ #
    #  Render
    # ------------------------------------------------------------------ #
    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        for obj in self.objects:
            obj.render()
