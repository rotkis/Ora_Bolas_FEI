import glm


class Light:
    def __init__(self, position=(0, 30, 10), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # intensities
        self.Ia = 0.25 * self.color  # ambient
        self.Id = 0.85 * self.color  # diffuse
        self.Is = 0.6 * self.color  # specular
