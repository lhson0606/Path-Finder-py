import Command as Command


class DeleteShapeCmd(Command):
    def __init__(self, shape):
        self.shape = shape
        self.deletedShape = None

    def execute(self):
        self.deletedShape = self.shape
        self.shape.delete()

    def unexecute(self):
        self.shape = self.deletedShape
        self.shape.undelete(