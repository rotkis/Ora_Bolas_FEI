import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[1] = self.get_texture(path='textures/img.png')
        self.textures[0] = self.get_texture(path='textures/img_1.png')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        '''
        self.textures['ball_w_roughness'] = self.get_texture(path='objects/ball/textures/Ball_White_s_Roughness.png')
        self.textures['ball_w_normal'] = self.get_texture(path='objects/ball/textures/Ball_White_s_Normal.png')
        self.textures['ball_w_metallic'] = self.get_texture(path='objects/ball/textures/Ball_White_s_Metallic.png')
        self.textures['ball_w_base'] = self.get_texture(path='objects/ball/textures/Ball_White_s_BaseColor.png')
        self.textures['ball_b_normal'] = self.get_texture(path='objects/ball/textures/Ball_Black_s_Normal.png')
        self.textures['ball_b_roughness'] = self.get_texture(path='objects/ball/textures/Ball_Black_s_Roughness.png')
        self.textures['ball_b_metallic'] = self.get_texture(path='objects/ball/textures/Ball_Black_s_Metallic.png')
        self.textures['ball_b_base'] = self.get_texture(path='objects/ball/textures/Ball_Black_s_BaseColor.png')

        ☻'''
    def load_ball_textures(self):
        ball_texture_paths = [
            'objects/ball/textures/Ball_White_s_Roughness.png',
            'objects/ball/textures/Ball_White_s_Normal.png',
            'objects/ball/textures/Ball_White_s_Metallic.png',
            'objects/ball/textures/Ball_White_s_BaseColor.png',
            'objects/ball/textures/Ball_Black_s_Normal.png',
            'objects/ball/textures/Ball_Black_s_Roughness.png',
            'objects/ball/textures/Ball_Black_s_Metallic.png',
            'objects/ball/textures/Ball_Black_s_BaseColor.png'
        ]
        for i, path in enumerate(ball_texture_paths):
            self.textures[f'ball_{i}'] = self.get_texture(path=path)

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]