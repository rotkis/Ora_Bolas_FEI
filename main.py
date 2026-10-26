"""
Ora Bolas — motor gráfico (OpenGL) e gerador de gráficos.

Uso:
    python3 main.py --gui                     # abre o launcher (padrão)
    python3 main.py --sim [--x X] [--z Z]     # abre a simulação 3D
    python3 main.py --graph all [--x X] [--z Z]
    python3 main.py --graph positions|velocity|acceleration|distance
"""

import argparse
import sys
from pathlib import Path

# Garante que o projeto é sempre rodado a partir da pasta dele
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pygame as pg
import moderngl as mgl

from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900), posicao=(0.0, 0.0)):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        self.WIN_SIZE = win_size
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Ora Bolas — Simulacao 3D")

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 1

        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self, posicao_x=posicao[0], posicao_z=posicao[1])
        self.running = True

    # ------------------------------------------------------------------ #
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_SPACE:
                    self.scene.toggle_animation()
                elif event.key == pg.K_r:
                    posicao = (self.scene.posicao_x, self.scene.posicao_z)
                    for obj in self.scene.objects:
                        del obj
                    self.scene = Scene(self, posicao_x=posicao[0], posicao_z=posicao[1])

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        pg.display.flip()

    def update_title(self):
        fps = self.clock.get_fps()
        status = "PAUSADO" if self.scene.animation_paused else "ANIMANDO"
        pg.display.set_caption(
            f"Ora Bolas 3D  |  {fps:5.1f} FPS  |  {status}  "
            f"|  Sair: ESC   Animacao: ESPACO   Reset: R"
        )

    def run(self):
        while self.running:
            self.time = pg.time.get_ticks() * 0.001
            self.scene.animar()
            self.check_events()
            self.camera.update()
            self.render()
            self.update_title()
            self.delta_time = max(self.clock.tick(60), 1)
        # libera os recursos da GPU antes de fechar a janela
        self.mesh.destroy()
        pg.quit()


def run_simulation(x: float, z: float):
    app = GraphicsEngine(posicao=(x, z))
    app.run()


def run_graphs(which: str, x: float, z: float):
    from graficos import Graphics

    graphics = Graphics(robo_x=x, robo_z=z)
    graphics.show(which)


def run_gui():
    from gui import OreBolasGui

    OreBolasGui().run()


def main():
    parser = argparse.ArgumentParser(description="Ora Bolas — simulacao e graficos")
    parser.add_argument("--gui", action="store_true", help="abre o launcher grafico")
    parser.add_argument("--sim", action="store_true", help="abre a simulacao 3D")
    parser.add_argument(
        "--graph", choices=["positions", "velocity", "acceleration", "distance", "all"]
    )
    parser.add_argument(
        "--x", type=float, default=0.0, help="posicao inicial X do robo (m)"
    )
    parser.add_argument(
        "--z", type=float, default=0.0, help="posicao inicial Z do robo (m)"
    )
    args = parser.parse_args()

    if args.graph:
        run_graphs(args.graph, args.x, args.z)
    elif args.sim:
        run_simulation(args.x, args.z)
    else:
        run_gui()


if __name__ == "__main__":
    main()
