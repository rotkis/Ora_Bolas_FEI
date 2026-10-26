import glm
import numpy as np


class BaseModel:
    def __init__(
        self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)
    ):
        self.app = app
        self.pos = glm.vec3(pos)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = glm.vec3(scale)
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = app.camera
        self.texture = app.mesh.texture.textures[tex_id]
        self.m_model = self.get_model_matrix()
        self.on_init()

    def on_init(self):
        self.program["u_texture_0"] = 0
        self.texture.use()
        # Matrizes de projeção/visão e luz (fixas durante a execução)
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)

    def get_model_matrix(self) -> glm.mat4:
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        return glm.scale(m_model, self.scale)

    def render(self):
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        self.texture.use()
        self.vao.render()


class StaticMesh(BaseModel):
    """Mesh estático grande (linhas do campo / piso)."""

    def __init__(self, app, vao_name, tex_id):
        super().__init__(app, vao_name, tex_id)

    def get_model_matrix(self) -> glm.mat4:
        return glm.mat4()

    def on_init(self):
        super().on_init()
        # m_model save: identidade — escrita única
        self.program["m_model"].write(self.m_model)


class Cat(BaseModel):
    def __init__(self, app, pos=(0, 0, 0), rot=(-90, -180, 0), scale=(2.0, 2.0, 2.0)):
        super().__init__(app, "cat", "cat", pos, rot, scale)


class Ball(BaseModel):
    def __init__(self, app, pos=(0, 0, 0), rot=(0, 0, 0), scale=(0.72, 0.72, 0.72)):
        super().__init__(app, "ball", "ball", pos, rot, scale)
