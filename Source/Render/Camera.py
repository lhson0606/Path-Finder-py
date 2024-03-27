import glm
import enum
import Source.Util.dy as dy

POS = glm.vec3(12, -10, 16)
DIR = glm.vec3(0, 0, 0) - POS

MOVE_SPEED = 20
MOUSE_SENSITIVITY = 0.05
PITCH_MAX_CONSTRAINT = 89.0
PITCH_MIN_CONSTRAINT = -89.0
FOV = 45.0
PITCH = -40
YAW = 90
WORLD_UP = glm.vec3(0, 0, 1)


class Camera:
    class Movement(enum.Enum):
        FORWARD = 0
        BACKWARD = 1
        LEFT = 2
        RIGHT = 3
        UP = 4
        DOWN = 5

    def __init__(self, pos=POS, up=WORLD_UP, yaw=YAW, pitch=PITCH):
        self.pos = glm.vec3(pos)
        self.dir = glm.normalize(glm.vec3(DIR))
        self.up = glm.normalize(glm.vec3(up))
        self.right = None

        self.yaw = yaw
        self.pitch = pitch

        self.mouse_sensitivity = MOUSE_SENSITIVITY
        self.fov = FOV

        self.view = None

        self.will_print_camera_info = False
        self.will_print_camera_using_imgui = False

        self.update_camera_vectors()

    def update_camera_vectors(self):
        self.dir.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.dir.y = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.dir.z = glm.sin(glm.radians(self.pitch))
        self.dir = glm.normalize(self.dir)

        self.right = glm.normalize(glm.cross(self.dir, WORLD_UP))
        self.up = glm.normalize(glm.cross(self.right, self.dir))

        self.view = glm.lookAt(self.pos, self.pos + self.dir, self.up)
        # self.view = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        if self.will_print_camera_info:
            self.print_camera_info()

        pass

    def print_camera_info(self):
        dy.log.info(f"=====Camera Info=====")
        dy.log.info(f"Position: {self.pos}")
        dy.log.info(f"Direction: {self.dir}")
        dy.log.info(f"Up: {self.up}")
        dy.log.info(f"Right: {self.right}")
        dy.log.info(f"Yaw: {self.yaw}")
        dy.log.info(f"Pitch: {self.pitch}")
        dy.log.info(f"FOV: {self.fov}")

    def process_keyboard(self, direction, dt):
        velocity = MOVE_SPEED * dt
        if direction == self.Movement.FORWARD:
            self.pos += self.dir * velocity
        if direction == self.Movement.BACKWARD:
            self.pos -= self.dir * velocity
        if direction == self.Movement.LEFT:
            self.pos -= self.right * velocity
        if direction == self.Movement.RIGHT:
            self.pos += self.right * velocity
        if direction == self.Movement.UP:
            self.pos += WORLD_UP * velocity
        if direction == self.Movement.DOWN:
            self.pos -= WORLD_UP * velocity

        self.update_camera_vectors()
        pass

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        d_x = x_offset*self.mouse_sensitivity
        d_y = y_offset*self.mouse_sensitivity

        self.yaw += d_x
        self.pitch += d_y

        if constrain_pitch:
            if self.pitch > PITCH_MAX_CONSTRAINT:
                self.pitch = PITCH_MAX_CONSTRAINT
            if self.pitch < PITCH_MIN_CONSTRAINT:
                self.pitch = PITCH_MIN_CONSTRAINT

        self.update_camera_vectors()
        pass

    def process_mouse_scroll(self, y_offset):
        if 1.0 <= self.fov <= 90.0:
            self.fov -= y_offset
        if self.fov <= 1.0:
            self.fov = 1.0
        if self.fov >= 90.0:
            self.fov = 90.0

        self.update_camera_vectors()

        pass
