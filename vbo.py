import numpy as np
import moderngl as mgl

from obj_loader import load_obj_static

# Geometria base do cubo (36 vértices x 8 floats: tex, normal, pos)
# é gerada UMA única vez e reutilizada por todos os meshes que a usam.
_CUBE_BASE: np.ndarray | None = None


def cube_base_data() -> np.ndarray:
    """Retorna a geometria do cubo unitário como array (36, 8) float32."""
    global _CUBE_BASE
    if _CUBE_BASE is None:
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]
        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        positions = np.array(
            [vertices[i] for tri in indices for i in tri], dtype=np.float32
        )

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]
        texcoords = np.array(
            [tex_coord_vertices[i] for tri in tex_coord_indices for i in tri],
            dtype=np.float32,
        )

        face_normals = [
            (0, 0, 1),
            (1, 0, 0),
            (0, 0, -1),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
        ]
        normals = np.repeat(np.array(face_normals, dtype=np.float32), 6, axis=0)

        _CUBE_BASE = np.hstack((texcoords, normals, positions)).astype(np.float32)
    return _CUBE_BASE


def bake_cubes(positions: np.ndarray, scale: float = 0.5) -> np.ndarray:
    """Combine N cubos (um por posição) em um único buffer de vértices.

    `positions` é um array (N, 3). A transformação (escala + translação) é
    'assada' nos vértices, permitindo desenhar todo o conjunto em 1 draw call.
    """
    base = cube_base_data()  # (36, 8)
    n = len(positions)
    data = np.tile(base, (n, 1))
    data = data.reshape(n, len(base), 8)
    data[:, :, 5:8] = base[None, :, 5:8] * scale + positions[:, None, :]
    return data.reshape(-1, 8).astype(np.float32)


class VBO:
    def __init__(self, ctx):
        self.vbos = {
            "cat": CatVBO(ctx),
            "ball": BallVBO(ctx),
            "field": FieldVBO(ctx),
            "floor": FloorVBO(ctx),
        }

    def destroy(self):
        for vbo in self.vbos.values():
            vbo.destroy()


class BaseVBO:
    format = "2f 3f 3f"
    attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = ctx.buffer(self.get_vertex_data())

    def get_vertex_data(self) -> np.ndarray: ...

    def destroy(self):
        self.vbo.release()


class CatVBO(BaseVBO):
    def get_vertex_data(self) -> np.ndarray:
        data = load_obj_static("objects/cat/20430_Cat_v1_NEW.obj")
        # Normaliza o modelo para ~1 unidade de altura, sem depender do OBJ.
        size = data[:, 5:8].max(axis=0) - data[:, 5:8].min(axis=0)
        data[:, 5:8] -= (data[:, 5:8].max(axis=0) + data[:, 5:8].min(axis=0)) * 0.5
        data[:, 5:8] /= size[1]
        return data.tobytes()


class BallVBO(BaseVBO):
    def get_vertex_data(self) -> np.ndarray:
        data = load_obj_static("objects/ball/10536_soccerball_V1_iterations-2.obj")
        size = data[:, 5:8].max(axis=0) - data[:, 5:8].min(axis=0)
        data[:, 5:8] -= (data[:, 5:8].max(axis=0) + data[:, 5:8].min(axis=0)) * 0.5
        data[:, 5:8] /= size.max()
        return data.tobytes()


class FieldVBO(BaseVBO):
    """Linhas do campo (37x46) — 1 draw call no lugar de ~250 cubos."""

    FIELD_W = 30
    FIELD_H = 45

    def get_vertex_data(self) -> np.ndarray:
        w, h = self.FIELD_W, self.FIELD_H
        area_x, area_z = 10, 5
        penalti_z = 9
        # Ligeiramente acima do piso (-1.5) para evitar z-fighting
        ys = -1.98

        lines = set()
        # contorno
        lines.update((x, ys, 0) for x in range(w + 1))
        lines.update((x, ys, h) for x in range(w + 1))
        lines.update((0, ys, z) for z in range(h + 1))
        lines.update((w, ys, z) for z in range(h + 1))
        # linha do meio
        lines.update((x, ys, h // 2) for x in range(w + 1))
        # áreas do gol
        lines.update((area_x, ys, y) for y in range(area_z + 1))
        lines.update((area_x, ys, h - y) for y in range(area_z + 1))
        lines.update((w - area_x, ys, y) for y in range(area_z + 1))
        lines.update((w - area_x, ys, h - y) for y in range(area_z + 1))
        lines.update((area_x + i, ys, area_z) for i in range(area_x + 1))
        lines.update((area_x + i, ys, h - area_z) for i in range(area_x + 1))
        # marca do pênalti
        for cx in (w // 2, w // 2):
            lines.add((cx, ys, penalti_z))
            lines.add((cx, ys, h - penalti_z))

        data = bake_cubes(np.array(sorted(lines), dtype=np.float32), scale=0.5)
        return data.tobytes()


class FloorVBO(BaseVBO):
    """Piso em malha 31x46 — 1 draw call no lugar de ~1400 cubos."""

    def get_vertex_data(self) -> np.ndarray:
        xs = np.arange(31, dtype=np.float32)
        zs = np.arange(46, dtype=np.float32)
        zz, xx = np.meshgrid(zs, xs)
        grid = np.column_stack(
            (xx.ravel(), np.full(xx.size, -2.0, np.float32), zz.ravel())
        )
        data = bake_cubes(grid, scale=0.5)
        return data.tobytes()
