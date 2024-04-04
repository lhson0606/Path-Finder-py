import OpenGL.GL as gl

import Source.Util.dy as dy

import ctypes


class PickInfo:
    def __init__(self):
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.entity: float = 0.0


class PickingFrame:
    def __init__(self, width, height):
        # probably move gl init to a different method
        self.fbo = gl.glGenFramebuffers(1)
        self.depth_texture = gl.glGenTextures(1)
        self.color_texture = gl.glGenTextures(1)
        self.width = width
        self.height = height

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.depth_texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, width, height, 0, gl.GL_DEPTH_COMPONENT,
                        gl.GL_FLOAT, ctypes.c_void_p(0))
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, self.depth_texture, 0)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.color_texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA32F, width, height, 0, gl.GL_RGBA, gl.GL_FLOAT, ctypes.c_void_p(0))
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.color_texture, 0)

        # Disable reading
        gl.glReadBuffer(gl.GL_NONE)

        gl.glDrawBuffer(gl.GL_COLOR_ATTACHMENT0)

        status = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)

        if status != gl.GL_FRAMEBUFFER_COMPLETE:
            dy.log.error("Framebuffer not complete")
            dy.log.error(status)
            raise Exception("Framebuffer not complete")

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def __del__(self):
        # gl.glDeleteFramebuffers(1, self.fbo)
        # gl.glDeleteTextures(1, self.depth_texture)
        # gl.glDeleteTextures(1, self.color_texture)
        pass

    def EnableWriting(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo)
        pass

    def DisableWriting(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        pass

    def GetPickInfo(self, x, y):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.fbo)
        gl.glReadBuffer(gl.GL_COLOR_ATTACHMENT0)

        pick_info = PickInfo()
        data = gl.glReadPixels(x, self.height - y, 1, 1, gl.GL_RGBA, gl.GL_FLOAT, None)

        pick_info.x = data[0][0][0]
        pick_info.y = data[0][0][1]
        pick_info.z = data[0][0][2]
        pick_info.entity = data[0][0][3]

        gl.glReadBuffer(gl.GL_NONE)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        return pick_info
