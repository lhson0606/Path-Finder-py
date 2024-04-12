import glm


class MotionComponent:
    def __init__(self, velocity: glm.vec3 = glm.vec3(0,0,0), distance: float = 0):
        self.start_position = glm.vec3(0.0, 0.0, 0.0)
        self.velocity = glm.vec3(velocity)
        self.distance = distance

    def set_velocity(self, velocity: glm.vec3):
        self.velocity = glm.vec3(velocity)
