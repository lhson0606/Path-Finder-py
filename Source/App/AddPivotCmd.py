import Source.App.Command as Command
import esper
import Source.Util.dy as dy
import glm


class AddPivotCommand(Command.Command):
    def __init__(self, shape_ent, pivot: glm.ivec3):
        pass

    def execute(self):
        dy.log.info("MoveCubeCmd execute")
        pass

    def undo(self):
        dy.log.info("MoveCubeCmd undo")
        pass
