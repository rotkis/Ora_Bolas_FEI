import moderngl as mgl


class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {
            "default": self.get_program("default"),
        }

    def get_program(self, name: str) -> mgl.Program:
        from pathlib import Path

        base = Path(__file__).resolve().parent / "shaders"
        with open(base / f"{name}.vert") as file:
            vert = file.read()
        with open(base / f"{name}.frag") as file:
            frag = file.read()
        return self.ctx.program(vertex_shader=vert, fragment_shader=frag)

    def destroy(self):
        for program in self.programs.values():
            program.release()
