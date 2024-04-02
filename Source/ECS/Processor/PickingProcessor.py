import ctypes

import esper

import Source.App.App as App

import Source.Util.dy as dy

import Source.Render.PickingFrame as PickingFrame

import Source.Render.Shader as Shader
import Source.Manager.ShaderManager as ShaderManager
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent

import OpenGL.GL as gl

class PickingProcessor(esper.Processor):
    def __init__(self, app: App):
        self.app = app
        self.picked_entity = None
        self.picking_shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.PICKING_DATA_SHADER)

    def pick(self, x, y):
        picking_frame = PickingFrame.PickingFrame(self.app.width, self.app.height)

        self.picking_shader.use()
        self.picking_shader.set_mat4("projection", self.app.projection)
        self.picking_shader.set_mat4("view", self.app.cur_map_context.camera.view)
        self.picking_shader.stop()

        picking_frame.EnableWriting()

        # disable blend?

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderManager.ShaderType.SHAPE_SHADER:
                    self.render_as_shape(ent, self.picking_shader)

        picking_frame.DisableWriting()

        # read pixel data
        data = picking_frame.GetPickInfo(x, y)

        dy.log.info("Picked data: " + str(data.entity))

        self.picked_entity = data.entity


        return self.picked_entity

        pass

    def process(self, dt):
        # self.pick(10, 10)
        pass

    def render_as_shape(self, ent, shader):
        shape_data = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
        vao = gl.glGenVertexArrays(1)
        vbo_pos = gl.glGenBuffers(1)
        vbo_normal = gl.glGenBuffers(1)
        vbo_id = gl.glGenBuffers(1)
        vbo_col0 = gl.glGenBuffers(1)
        vbo_col1 = gl.glGenBuffers(1)
        vbo_col2 = gl.glGenBuffers(1)
        vbo_col3 = gl.glGenBuffers(1)
        ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_pos)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_position(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_normal)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_normal(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_id(), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(2, 1, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(2)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_col0)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_transform(0), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(3, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(3)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_col1)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_transform(1), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(4, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(4)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_col2)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_transform(2), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(5, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(5)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_col3)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, shape_data.get_batch_picking_transform(3), gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(6, 4, gl.GL_FLOAT, gl.GL_FALSE, 0, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(6)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, shape_data.get_batch_picking_indices(), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(0)

        shader.use()
        shader.set_mat4("view", self.app.cur_map_context.camera.view)
        shader.set_mat4("projection", self.app.projection)
        gl.glBindVertexArray(vao)
        gl.glDrawElements(gl.GL_TRIANGLES, shape_data.vertex_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()

        # clean up
        # gl.glDeleteVertexArrays(1, vao)
        # gl.glDeleteBuffers(1, vbo_pos)
        # gl.glDeleteBuffers(1, vbo_normal)
        # gl.glDeleteBuffers(1, vbo_id)
        # gl.glDeleteBuffers(1, vbo_col0)
        # gl.glDeleteBuffers(1, vbo_col1)
        # gl.glDeleteBuffers(1, vbo_col2)
        # gl.glDeleteBuffers(1, vbo_col3)
        # gl.glDeleteBuffers(1, ebo)

        pass
