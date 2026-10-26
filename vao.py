from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {
            "cat": self.get_vao(
                program=self.program.programs["default"], vbo=self.vbo.vbos["cat"]
            ),
            "ball": self.get_vao(
                program=self.program.programs["default"], vbo=self.vbo.vbos["ball"]
            ),
            "field": self.get_vao(
                program=self.program.programs["default"], vbo=self.vbo.vbos["field"]
            ),
            "floor": self.get_vao(
                program=self.program.programs["default"], vbo=self.vbo.vbos["floor"]
            ),
        }

    def get_vao(self, program, vbo):
        return self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])

    def destroy(self):
        for vao in self.vaos.values():
            vao.release()
        self.vbo.destroy()
        self.program.destroy()
