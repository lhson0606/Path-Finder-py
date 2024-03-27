import glm


class TransformComponent:
    def __init__(self, position: glm.vec3):
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self._local_matrix = glm.mat4(1)
        self._world_matrix = glm.mat4(1)
        self.update_world_matrix()

    def get_world_transform(self):
        return self._world_matrix

    def update_world_matrix(self):
        _world_matrix = glm.mat4(1)
        _world_matrix = glm.translate(_world_matrix, self.position)
        _world_matrix = glm.rotate(_world_matrix, self.rotation.x, glm.vec3(1, 0, 0))
        _world_matrix = glm.rotate(_world_matrix, self.rotation.y, glm.vec3(0, 1, 0))
        _world_matrix = glm.rotate(_world_matrix, self.rotation.z, glm.vec3(0, 0, 1))
        _world_matrix = glm.scale(_world_matrix, self.scale)
        pass

