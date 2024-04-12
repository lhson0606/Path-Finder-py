import logging
import os.path
import glm
import math

# referenced https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


def read_text(file_path):
    if not os.path.exists(file_path):
        log.error(f"File not found: {file_path}")
        return ""

    with open(file_path, 'r') as file:
        return file.read()


def file_exists(path):
    return os.path.exists(path)


def cast_ray(mouse_x: float, mouse_y: float, width: int, height: int, view: glm.mat4, projection: glm.mat4) -> glm.vec3:
    # convert mouse position to NDC
    x = (2.0 * mouse_x) / width - 1.0
    y = 1.0 - (2.0 * mouse_y) / height
    z = 1.0

    ray_nds = glm.vec3(x, y, z)
    ray_clip = glm.vec4(ray_nds.x, ray_nds.y, -1.0, 1.0)
    ray_eye = glm.inverse(projection) * ray_clip
    ray_eye = glm.vec4(ray_eye.x, ray_eye.y, -1.0, 0.0)
    ray_world = glm.inverse(view) * ray_eye
    ray_world = glm.normalize(glm.vec3(ray_world))

    return ray_world


def round_away_from_zero(value):
    return math.ceil(value) if value > 0 else math.floor(value)

def get_safe_direction(v: glm.vec3):
    if v.x == 0 and v.y == 0 and v.z == 0:
        return glm.vec3(0, 0, 0)

    return glm.normalize(v)
