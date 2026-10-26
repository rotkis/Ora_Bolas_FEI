from PIL import Image
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {
            1: self.get_texture("textures/img.png"),
            0: self.get_texture("textures/img_1.png"),
            2: self.get_texture("textures/img_2.png"),
            "cat": self.get_texture("objects/cat/20430_cat_diff_v1.jpg"),
            "ball": self.get_texture("objects/ball/10536_soccerball_V1_diffuse.jpg"),
        }

    def get_texture(self, path: str) -> mgl.Texture:
        # Pillow em vez de pygame: não depende de display SDL inicializado e
        # evita o caminho legado pygame.image.tostring.
        image = Image.open(path).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
        texture = self.ctx.texture(size=image.size, components=3, data=image.tobytes())
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # Anisotropic filter (limitado ao máximo suportado pelo driver)
        max_af = self.ctx.info.get("MAX_TEXTURE_ANISOTROPY", 8.0)
        texture.anisotropy = min(8.0, max_af)
        return texture

    def destroy(self):
        for texture in self.textures.values():
            texture.release()
