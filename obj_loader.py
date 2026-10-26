"""
Loader mínimo de arquivos OBJ (com v/vt/vn e faces).

Substitui a biblioteca pywavefront (que não funciona mais no Python 3.14 / Linux)
e gera os vértices já expandidos por triângulo, no mesmo layout usado pelos
shaders do projeto: '2f 3f 3f'  ->  texcoord(2), normal(3), position(3).
"""

import numpy as np


def load_obj(path: str) -> np.ndarray:
    """Carrega um OBJ e devolve um array (n_triangulos*3, 8) float32.

    Colunas: [tex_u, tex_v, n_x, n_y, n_z, x, y, z]
    Faces não trianguladas (quads/ngons) são divididas em leque de triângulos.
    """
    positions: list[tuple] = []
    texcoords: list[tuple] = []
    normals: list[tuple] = []
    faces: list[list[tuple]] = []

    with open(path, "r") as file:
        for line in file:
            if len(line) < 3 or line.startswith("#"):
                continue
            parts = line.split()
            key = parts[0]
            if key == "v":
                positions.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif key == "vt":
                texcoords.append((float(parts[1]), float(parts[2])))
            elif key == "vn":
                normals.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif key == "f":
                corners = []
                for token in parts[1:]:
                    v, t, n = (token.split("/") + ["", ""])[:3]
                    corners.append((int(v), int(t), int(n)))
                faces.append(corners)

    if not faces or not positions:
        raise ValueError(f"OBJ sem faces ou vértices: {path}")

    # Converte para arrays numpy para acesso rápido (indexação em lote).
    pos = np.array(positions, dtype=np.float32)
    tex = (
        np.array(texcoords, dtype=np.float32)
        if texcoords
        else np.zeros((1, 2), np.float32)
    )
    nor = (
        np.array(normals, dtype=np.float32) if normals else np.zeros((1, 3), np.float32)
    )
    no_tex = not texcoords
    no_norm = not normals

    rows = np.empty((sum(3 * (len(f) - 2) for f in faces), 8), dtype=np.float32)
    out = rows  # alias

    def index_to_int(value: str, count: int) -> int:
        # OBJ usa índices a partir de 1 (ou negativos, relativos ao fim).
        i = int(value)
        return min(max(i - 1 if i > 0 else count + i, 0), count - 1)

    w = 0
    for corners in faces:
        n = len(corners)
        # triangulação em leque: (c0, ck, ck+1)
        for k in range(1, n - 1):
            for c in (corners[0], corners[k], corners[k + 1]):
                vi = index_to_int(c[0], len(positions)) if c[0] else 0
                ti = index_to_int(c[1], len(texcoords)) if c[1] else 0
                ni = index_to_int(c[2], len(normals)) if c[2] else 0
                out[w, 0:2] = (0.0, 0.0) if no_tex else tex[ti]
                out[w, 2:5] = (0.0, 1.0, 0.0) if no_norm else nor[ni]
                out[w, 5:8] = pos[vi]
                w += 1
    return rows[:w]


def load_obj_static(path: str) -> np.ndarray:
    """Mesma coisa que load_obj, porém usando um cache em disco (.obj.cache.npy).

    O parse puro do OBJ demora ~1s em modelos grandes (98k faces). O cache
    torna as inicializações seguintes praticamente instantâneas e é
    regenerado automaticamente se o .obj mudar.
    """
    from pathlib import Path

    src = Path(path)
    cache = src.with_suffix(src.suffix + ".cache.npy")
    if cache.exists() and cache.stat().st_mtime >= src.stat().st_mtime:
        return np.load(cache)
    data = load_obj(path)
    try:
        np.save(cache, data)
    except OSError:
        pass
    return data
