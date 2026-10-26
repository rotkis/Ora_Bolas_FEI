"""
Ora Bolas — Launcher (janela de abertura).

Permite definir a posição inicial do robô e abrir o que quiser:
  * Simulação 3D
  * Todos os gráficos
  * Gráfico de posições / velocidades / acelerações / distância (cada um)

Cada item abre em um processo separado, então dá para deixar a janela 3D
rodando e ir abrindo os gráficos ao mesmo tempo.
"""

import os
import subprocess
import sys

import pygame as pg

from pathlib import Path

# SDL em janelas 2D puras renderiza com "furos" no Wayland/Hyprland;
# via XWayland fica opaco e correto.
os.environ.setdefault("SDL_VIDEODRIVER", "x11")

BASE_DIR = Path(__file__).resolve().parent

BG = (24, 27, 33)
PANEL = (34, 39, 48)
PANEL_HOVER = (46, 54, 66)
ACCENT = (86, 156, 105)
TEXT = (232, 236, 241)
TEXT_DIM = (150, 158, 168)
ACTIVE = (86, 120, 156)


class Entry:
    """Campo de texto simples (números)."""

    def __init__(self, rect, default=""):
        self.rect = pg.Rect(rect)
        self.text = default
        self.active = False

    def handle(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode in "0123456789.-+":
                self.text += event.unicode

    def draw(self, screen, font):
        border = ACCENT if self.active else TEXT_DIM
        shadow_box(screen, self.rect, PANEL, border)
        color = border if not self.active else TEXT
        label = font.render(self.text, True, color)
        screen.blit(
            label,
            (self.rect.x + 10, self.rect.y + (self.rect.h - label.get_height()) // 2),
        )


class Button:
    def __init__(self, rect, label, callback, font):
        self.rect = pg.Rect(rect)
        self.label = label
        self.callback = callback
        self.font = font

    def draw(self, screen):
        hover = self.rect.collidepoint(pg.mouse.get_pos())
        color = ACCENT if hover else PANEL
        shadow_box(screen, self.rect, color, TEXT if hover else TEXT_DIM)
        text = self.font.render(self.label, True, TEXT)
        screen.blit(
            text,
            (
                self.rect.x + (self.rect.w - text.get_width()) // 2,
                self.rect.y + (self.rect.h - text.get_height()) // 2,
            ),
        )

    def handle(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()


def shadow_box(screen, rect, color, border):
    pg.draw.rect(screen, color, rect, border_radius=8)
    pg.draw.rect(screen, border, rect, 2, border_radius=8)


class OreBolasGui:
    def __init__(self, win_size=(980, 620)):
        pg.init()
        self.win_size = win_size
        self.screen = pg.display.set_mode(win_size)
        pg.display.set_caption("Ora Bolas — Launcher")
        self.clock = pg.time.Clock()
        self.font = self.load_font(26)
        self.font_small = self.load_font(20)

        m = 40  # margem
        gap = 14
        w = (win_size[0] - 2 * m - gap) / 2

        # Entrada da posição do robô
        entry_y = 105
        self.label_x = self.font_small.render("X do robô (m):", True, TEXT_DIM)
        self.label_z = self.font_small.render("Z do robô (m):", True, TEXT_DIM)
        self.entry_x = Entry((m, entry_y, w, 44), "0.0")
        self.entry_z = Entry((m + w + gap, entry_y, w, 44), "0.0")

        # Layout dos botões em grade 2 colunas
        self.buttons = []
        rows = [
            ("Simulação 3D", self.open_sim),
            ("Todos os gráficos", lambda: self.open_graph("all")),
            ("Gráfico — Posições", lambda: self.open_graph("positions")),
            ("Gráfico — Distância", lambda: self.open_graph("distance")),
            ("Gráfico — Velocidades", lambda: self.open_graph("velocity")),
            ("Gráfico — Acelerações", lambda: self.open_graph("acceleration")),
        ]
        for i, (label, action) in enumerate(rows):
            row, col = divmod(i, 2)
            x = m + col * (w + gap)
            y = 190 + row * 76
            self.buttons.append(
                Button((round(x), y, round(w), 62), label, action, self.font)
            )

        self.status = "Pronto. Clique em algo para abrir em nova janela."
        self.status_color = ACCENT

    @staticmethod
    def load_font(size):
        for name in ("dejavusans", "ubuntumono", "notosans"):
            try:
                return pg.font.SysFont(name, size)
            except Exception:
                continue
        return pg.font.Font(None, int(size * 1.4))

    # ------------------------------------------------------------------ #
    def read_position(self):
        try:
            return float(self.entry_x.text.replace(",", ".")), float(
                self.entry_z.text.replace(",", ".")
            )
        except ValueError:
            self.status = "Posição inválida — use números, ex.: 0.0 e 1.0"
            self.status_color = (220, 90, 90)
            return None

    def open_sim(self):
        pos = self.read_position()
        if pos:
            self.launch(
                ["--sim", "--x", str(pos[0]), "--z", str(pos[1])],
                "Simulação 3D aberta em nova janela.",
            )

    def open_graph(self, which: str):
        pos = self.read_position()
        if pos:
            self.launch(
                ["--graph", which, "--x", str(pos[0]), "--z", str(pos[1])],
                f'Gráfico "{which}" aberto em nova janela.',
            )

    def launch(self, extra_args, message):
        cmd = [sys.executable, str(BASE_DIR / "main.py"), *extra_args]
        # filho SEM SDL_VIDEODRIVER=x11: simulação 3D fica melhor no Wayland nativo
        env = {k: v for k, v in os.environ.items() if k != "SDL_VIDEODRIVER"}
        subprocess.Popen(cmd, cwd=BASE_DIR, env=env)
        self.status = message
        self.status_color = ACCENT

    # ------------------------------------------------------------------ #
    def draw(self):
        self.screen.fill(BG)

        title = self.font.render("Ora Bolas", True, TEXT)
        self.screen.blit(title, (40, 26))
        sub = self.font_small.render(
            "Simulador de perseguição — robô x bola", True, TEXT_DIM
        )
        self.screen.blit(sub, (40 + title.get_width() + 14, 34))

        self.screen.blit(self.label_x, (42, self.entry_x.rect.y - 26))
        self.screen.blit(
            self.label_z, (self.entry_z.rect.x + 2, self.entry_z.rect.y - 26)
        )
        self.entry_x.draw(self.screen, self.font)
        self.entry_z.draw(self.screen, self.font)

        for button in self.buttons:
            button.draw(self.screen)

        status = self.font_small.render(self.status, True, self.status_color)
        self.screen.blit(status, (40, self.win_size[1] - 44))
        help_text = self.font_small.render(
            "3D: WASD move · mouse gira · ESPAÇO pausa · R reinicia · ESC sai",
            True,
            TEXT_DIM,
        )
        self.screen.blit(
            help_text, (40 + status.get_width() + 16, self.win_size[1] - 44)
        )

        pg.display.flip()

    def handle(self, event):
        self.entry_x.handle(event)
        self.entry_z.handle(event)
        for button in self.buttons:
            if event.type == pg.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                button.callback()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    running = False
                else:
                    self.handle(event)
            self.draw()
            self.clock.tick(60)
        pg.quit()


if __name__ == "__main__":
    OreBolasGui().run()
