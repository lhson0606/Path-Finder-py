import esper

import Source.Map.Map as Map
import Source.App as App
from abc import ABC, abstractmethod
import Source.ECS.Component.PathComponent as PathComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.ECS.Component.RenderComponent as RenderComponent



class VisualizedAlgorithm(ABC):
    def __init__(self, m: Map, app: App):
        self.map = m
        self.app = app
        self.path_ent = esper.create_entity(PathComponent.PathComponent(app))

        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.PATH_POINT_SHADER)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.PATH_POINT_SHADER, shader)

        esper.add_component(self.path_ent, render_comp)

    @abstractmethod
    def find_path(self):
        pass

    def solve_and_visualize(self):
        path_comp = esper.component_for_entity(self.path_ent, PathComponent.PathComponent)
        positions = self.find_path()

        if positions is None:
            self.app.pop_up_error("No path found")
            return

        path_comp.build_path(positions)

    def clean_up(self):
        path_comp = esper.component_for_entity(self.path_ent, PathComponent.PathComponent)
        path_comp.clean_up()
        pass
