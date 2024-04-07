import Source.App.Command as Command
import Source.ECS.Component.ShapeComponent
import esper
import Source.Util.dy as dy
import glm


class AddPivotCommand(Command.Command):
    def __init__(self, shape_ent, pivot: glm.ivec3):
        self.shape_ent = shape_ent
        self.pivot = pivot
        self.new_pivot_ent = -1
        pass

    def execute(self):
        shape_data = esper.component_for_entity(self.shape_ent, Source.ECS.Component.ShapeComponent.ShapeComponent)
        self.new_pivot_ent = shape_data.add_pivot(self.pivot)
        pass

    def undo(self):
        shape_data = esper.component_for_entity(self.shape_ent, Source.ECS.Component.ShapeComponent.ShapeComponent)
        shape_data.remove_pivot(shape_data.pivots.__len__()-1, self.new_pivot_ent)
        pass
