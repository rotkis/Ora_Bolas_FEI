from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        
        add(Cube(app, pos=(0, -2, -10)))

        add(Cat(app, pos=(0, -1, -10)))

        add(Ball(app, pos=(0, -2, -8)))

    def render(self):
        for obj in self.objects:
            obj.render()