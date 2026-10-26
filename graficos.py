"""
Gráficos do Ora Bolas: posição, velocidade, aceleração e distância.

Todos os cálculos foram vetorizados com numpy (antes ficavam em loops
Python) e a leitura da trajetória é feita uma única vez, já convertendo
os números "0,5" para float.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path

# Backend com interface gráfica:(Qt QtAgg incluído via PyQt6); o Tk do sistema
# não existe em todas as distros Linux.
try:
    matplotlib.use("QtAgg")
except Exception:
    pass

DT = 0.02  # passo de tempo da simulação (s)
ROBO_VEL_MAX = 2.8  # m/s
RAIO_INTERCEPTACAO = 0.0943  # m


class Graphics:
    def __init__(self, robo_x=0.0, robo_z=0.0):
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

        self.robo_x = robo_x
        self.robo_z = robo_z
        self.tempo = []
        self.interceptado_em = None

        self.temp(robo_x, robo_z)
        self.calcula_velocidade()
        self.calcula_aceleracao()

    # ------------------------------------------------------------------ #
    #  Simulação da perseguição do robô
    # ------------------------------------------------------------------ #
    def temp(self, x_robo: float, y_robo: float):
        velocidade_robo = ROBO_VEL_MAX
        tempo_s = 0.0

        path = Path(__file__).resolve().parent / "ball_trajectory.txt"
        data = np.genfromtxt(
            path,
            converters={i: lambda s: float(s.replace(",", ".")) for i in range(4)},
        )

        raio = RAIO_INTERCEPTACAO
        for linha in data:
            _, x_ball, y_ball, _ = linha
            dx = x_ball - x_robo
            dy = y_ball - y_robo
            norma = math_hypot(dx, dy)
            if norma == 0:
                norma = 1e-9

            x_robo += dx / norma * velocidade_robo * DT
            y_robo += dy / norma * velocidade_robo * DT

            self.trajetoria_robo.append((x_robo, y_robo))
            self.trajetoria_bola.append((x_ball, y_ball))
            self.posicao_x_robo.append(x_robo)
            self.posicao_z_robo.append(y_robo)
            self.posicao_x_bola.append(x_ball)
            self.posicao_z_bola.append(y_ball)
            self.tempo.append(tempo_s)
            self.distancias.append(math_hypot(x_robo - x_ball, y_robo - y_ball))

            if self.distancias[-1] <= raio:
                self.interceptado_em = tempo_s
                print(
                    f"O robô alcançou a bola no tempo {tempo_s:.2f}s, "
                    f"na posição [{x_robo:.3f}, {y_robo:.3f}]"
                )
                break
            tempo_s += DT

    # ------------------------------------------------------------------ #
    #  Cinemática (vetorizada)
    # ------------------------------------------------------------------ #
    def calcula_velocidade(self):
        robo = np.asarray(self.trajetoria_robo)
        bola = np.asarray(self.trajetoria_bola)
        v_robo = np.diff(robo, axis=0) / DT
        v_bola = np.diff(bola, axis=0) / DT

        # limita a velocidade do robô a ROBO_VEL_MAX (norma do vetor)
        norma_robo = np.linalg.norm(v_robo, axis=1, keepdims=True)
        v_robo = np.where(
            norma_robo > ROBO_VEL_MAX,
            v_robo * ROBO_VEL_MAX / np.maximum(norma_robo, 1e-9),
            v_robo,
        )

        self.velocidades_robo = v_robo
        self.velocidades_bola = v_bola

    def calcula_aceleracao(self):
        a_robo = np.diff(self.velocidades_robo, axis=0) / DT
        a_bola = np.diff(self.velocidades_bola, axis=0) / DT
        self.aceleracao_robo = a_robo
        self.aceleracao_bola = a_bola

    # ------------------------------------------------------------------ #
    #  Gráficos
    # ------------------------------------------------------------------ #
    def _suptitle(self) -> str | None:
        if self.interceptado_em is not None:
            return f"Interceptação em t = {self.interceptado_em:.2f}s"
        return None

    def show_posicoes(self, ax):
        ax.plot(self.tempo, self.posicao_x_bola, label="Posição x da bola")
        ax.plot(self.tempo, self.posicao_z_bola, label="Posição y da bola")
        ax.plot(self.tempo, self.posicao_x_robo, label="Posição x do robô")
        ax.plot(self.tempo, self.posicao_z_robo, label="Posição y do robô")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Posição")
        ax.set_title("Posição da bola e do robô em função do tempo")
        ax.legend()
        ax.grid(True)

    def show_velocidades(self, ax):
        t = self.tempo[1:]
        ax.plot(t, self.velocidades_robo[:, 0], label="Robô vx")
        ax.plot(t, self.velocidades_robo[:, 1], label="Robô vy")
        ax.plot(t, self.velocidades_bola[:, 0], label="Bola vx")
        ax.plot(t, self.velocidades_bola[:, 1], label="Bola vy")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Velocidade")
        ax.set_title("Componentes da velocidade da bola e do robô")
        ax.legend()
        ax.grid(True)

    def show_aceleracoes(self, ax):
        t = self.tempo[2:]
        ax.plot(t, self.aceleracao_robo[:, 0], label="Robô ax")
        ax.plot(t, self.aceleracao_robo[:, 1], label="Robô ay")
        ax.plot(t, self.aceleracao_bola[:, 0], label="Bola ax")
        ax.plot(t, self.aceleracao_bola[:, 1], label="Bola ay")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Aceleração")
        ax.set_title("Componentes da aceleração da bola e do robô")
        ax.legend()
        ax.grid(True)

    def show_distancia(self, ax):
        ax.plot(self.tempo, self.distancias, label="Distância")
        ax.set_xlabel("Tempo (s)")
        ax.set_ylabel("Distância")
        ax.set_title("Distância entre a bola e o robô")
        ax.legend()
        ax.grid(True)

    def show(self, which: str):
        """Mostra 'all', ou um gráfico só ('positions', 'velocity', ...)."""
        if which == "all":
            fig, axs = plt.subplots(2, 2, figsize=(13, 9))
            self.show_posicoes(axs[0][0])
            self.show_velocidades(axs[0][1])
            self.show_aceleracoes(axs[1][0])
            self.show_distancia(axs[1][1])
        else:
            fig, ax = plt.subplots(figsize=(9, 7))
            {
                "positions": self.show_posicoes,
                "velocity": self.show_velocidades,
                "acceleration": self.show_aceleracoes,
                "distance": self.show_distancia,
            }[which](ax)

        fig.suptitle(self._suptitle() or "Ora Bolas")
        fig.tight_layout(rect=(0, 0, 1, 0.95) if which == "all" else (0, 0, 1, 0.93))
        plt.show()


def math_hypot(x, y) -> float:
    return float(np.hypot(x, y))
