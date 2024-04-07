import Source.App.Command as Command
import esper
import Source.Util.dy as dy
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.CubeComponent as CubeComponent
import glm

class MoveCubeCmd(Command.Command):
    def __init__(self, ent_id, position: glm.vec3):
        self.entity = ent_id
        self.position = position
        self.old_position = None


    def execute(self):
        pos_comp = esper.component_for_entity(self.entity, TransformComponent.TransformComponent)
        cube_comp = esper.component_for_entity(self.entity, CubeComponent.CubeComponent)
        self.old_position = pos_comp.position
        pos_comp.set_position(self.position)
        shape_ent = cube_comp.shape_entity
        shape_comp = esper.component_for_entity(shape_ent, ShapeComponent.ShapeComponent)
        shape_comp.move_pivot(cube_comp.pivot_index, self.position)
        pass

    def undo(self):
        pos_comp = esper.component_for_entity(self.entity, TransformComponent.TransformComponent)
        pos_comp.set_position(self.old_position)
        cube_comp = esper.component_for_entity(self.entity, CubeComponent.CubeComponent)
        shape_ent = cube_comp.shape_entity
        shape_comp = esper.component_for_entity(shape_ent, ShapeComponent.ShapeComponent)
        shape_comp.move_pivot(cube_comp.pivot_index, self.old_position)
        pass