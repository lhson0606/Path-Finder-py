import OpenGL.GL as gl
import esper
from OpenGL.GLU import *

import Source.App.App as App
import Source.ECS.Component.GridComponent as GridComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.ECS.Component.TempShapeComponent as TempShapeComponent
import Source.ECS.Component.SkyBoxComponent as SkyBoxComponent
import Source.ECS.Component.OutliningComponent as OutliningComponent
import Source.Render.Shader as Shader
from Source.Manager.ShaderManager import ShaderType as ShaderType

import glm


class RenderProcessor(esper.Processor):
    def __init__(self, app: App):
        # hold a reference to the app to access necessary components
        self.app = app

    def process(self, dt):
        gl.glStencilMask(0x00)

        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderType.SKY_BOX_SHADER:
                    self.render_as_skybox(ent, render_data.shader)
        pass

        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderType.SHAPE_SHADER:
                    self.render_as_shape(ent, render_data.shader)
        pass

        # render all entities with render component
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderType.TEMP_SHAPE_SHADER:
                    self.render_as_temp_shape(ent, render_data.shader)



        # render all entities with render component
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderType.GRID_SHADER:
                    self.render_as_grid(ent, render_data.shader)

    def render_as_grid(self, ent, shader: Shader):
        gl.glDisable(gl.GL_CULL_FACE)
        shader.use()
        grid_data = esper.component_for_entity(ent, GridComponent.GridComponent)
        gl.glBindVertexArray(grid_data.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()
        gl.glEnable(gl.GL_CULL_FACE)
        pass

    def render_as_shape(self, ent, shader):
        # check for outlining
        outline_comp = esper.component_for_entity(ent, OutliningComponent.OutliningComponent)

        if outline_comp.will_draw_outline():
            gl.glStencilFunc(gl.GL_ALWAYS, 1, 0xFF)
            gl.glStencilMask(0xFF)

        # skybox
        sky_box_ent, skybox_comp = esper.get_component(SkyBoxComponent.SkyBoxComponent)[0]
        tex = skybox_comp.texture

        shader.use()

        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, tex)

        shader.set_vec3("cameraPos", self.app.cur_map_context.camera.pos)
        shape_data = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
        gl.glBindVertexArray(shape_data.vao)
        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, shape_data.vertex_count)
        gl.glDrawElements(gl.GL_TRIANGLES, shape_data.vertex_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()

        # draw outline if necessary
        if not outline_comp.will_draw_outline():
            return

        outline_shader = outline_comp.shader
        gl.glStencilFunc(gl.GL_NOTEQUAL, 1, 0xFF)
        gl.glStencilMask(0x00)
        gl.glDisable(gl.GL_DEPTH_TEST)

        outline_shader.use()

        outline_shader.set_mat4("projection", self.app.projection)
        outline_shader.set_mat4("view", self.app.cur_map_context.camera.view)

        gl.glBindVertexArray(shape_data.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, shape_data.vertex_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        outline_shader.stop()

        # reset state
        gl.glStencilMask(0xFF)
        gl.glStencilFunc(gl.GL_ALWAYS, 0, 0xFF)
        gl.glEnable(gl.GL_DEPTH_TEST)
        pass

    def render_as_temp_shape(self, ent, shader):
        temp_shape_data = esper.component_for_entity(ent, TempShapeComponent.TempShapeComponent)
        shader.use()
        gl.glBindVertexArray(temp_shape_data.vao)
        shader.set_mat4("projection", self.app.projection)
        shader.set_mat4("view", self.app.cur_map_context.camera.view)
        gl.glDrawElements(gl.GL_TRIANGLES, temp_shape_data.vertex_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()
        pass

    def update_projection(self, projection: glm.mat4):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader = render_data.shader
            shader.use()
            shader.set_mat4("projection", projection)
            shader.stop()
        pass

    def update_view(self, view: glm.mat4):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader = render_data.shader
            shader.use()
            shader.set_mat4("view", view)
            shader.stop()
        pass

    def update_grid_view(self, width, height):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            if shader_type == ShaderType.GRID_SHADER:
                shader = render_data.shader
                shader.use()
                shader.set_float("gridWidth", width)
                shader.set_float("gridHeight", height)
                shader.stop()
        pass

    def render_as_skybox(self, ent, shader):
        # gl.glDisable(gl.GL_CULL_FACE)
        # gl.glDepthMask(gl.GL_FALSE)
        # gl.glDisable(gl.GL_BLEND)
        gl.glDepthFunc(gl.GL_LEQUAL)

        shader.use()
        shader.set_mat4("projection", self.app.projection)
        sky_box_view = glm.mat4(glm.mat3(self.app.cur_map_context.camera.view))
        shader.set_mat4("view", sky_box_view)
        skybox_data = esper.component_for_entity(ent, SkyBoxComponent.SkyBoxComponent)
        gl.glBindVertexArray(skybox_data.vao)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, skybox_data.texture)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, skybox_data.vertex_count)
        gl.glBindVertexArray(0)
        shader.stop()

        # gl.glDepthMask(gl.GL_TRUE)
        # gl.glEnable(gl.GL_CULL_FACE)
        # gl.glEnable(gl.GL_BLEND)
        gl.glDepthFunc(gl.GL_LESS)
        pass

