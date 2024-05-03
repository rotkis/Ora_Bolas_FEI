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
        
        for i in range(49):
            if(i % 2 == 0):
                add(Cube(app, pos=(i, -2, -10)))
                add(Cube(app, pos=(i, -2, 80)))
            if (i % 16 == 0):
                add(Cube(app, pos=(i, -2, -8)))
                add(Cube(app, pos=(i, -2, 78)))

        for i in range(46):
            if(i % 2 == 0):
                add(Cube(app, pos=(0, -2, i-6)))
                add(Cube(app, pos=(0, -2, 76-i)))
                add(Cube(app, pos=(48, -2, i-6)))
                add(Cube(app, pos=(48, -2, 76-i)))

        for i in range(15):
            if (i% 2 == 0):
                add(Cube(app, pos=(16, -2, i-6)))
                add(Cube(app, pos=(32, -2, i-6)))
                add(Cube(app, pos=(16, -2, 76-i)))
                add(Cube(app, pos=(32, -2, 76-i)))
        
        for i in range(15):
            if (i% 2 == 0):
                add(Cube(app, pos=(16+i, -2, 8)))
                add(Cube(app, pos=(16+i, -2, 62)))

        add(Cube(app, pos=(24, -2, 4)))
        add(Cube(app, pos=(24, -2, 66)))


        for i in range(49):
            if(i % 2 == 0):
                if ( i != 0 or i != 48):
                    add(Cube(app, pos=(i, -2, 34)))
            if (i % 16 == 0):
                if ( i != 0 or i != 48):
                    add(Cube(app, pos=(i, -2, 36)))
                    add(Cube(app, pos=(i, -2, 32)))

        for i in range(9):
            if(i % 2 == 0):
                add(Cube(app, pos=(16, -2, 38+i)))
                add(Cube(app, pos=(16, -2, 30-i)))
                add(Cube(app, pos=(32, -2, 38+i)))
                add(Cube(app, pos=(32, -2, 30-i)))
        for i in range(15):
            if(i % 2 == 0):
                add(Cube(app, pos=(16+i, -2, 22)))
                add(Cube(app, pos=(16+i, -2, 46)))

        for i in range(49):
            for j in range(46):
                if(i % 2 == 0 and j % 2 ==0):
                    add(Cobe(app, pos=(i, -2, -8+j)))
                    add(Cobe(app, pos=(i, -2, 78-j)))


        

        add(Cat(app, pos=(10, -1, 20), rot=(-90, 0,0)))
        for i in range(100):
            if(i % 10 == 0):
                add(Ball(app, pos=(i, 0, i-8)))

    def render(self):
        for obj in self.objects:
            obj.render()