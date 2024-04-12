import esper
import glm

import Source.ECS.Component.MotionComponent as MotionComponent
import Source.ECS.Component.NameTagComponent as NameTagComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.TransformComponent as TransformComponent
import Source.Util.dy as dy


class PhysicProcessor(esper.Processor):

    def __init__(self):
        self._accumulated_time = 0
        self._is_enabled = False
        pass

    def enable(self):
        self._is_enabled = True
        pass

    def disable(self):
        self._is_enabled = False
        pass

    def process(self, dt):
        if not self._is_enabled:
            return

        self._accumulated_time = self._accumulated_time + dt

        if self._accumulated_time < 1.0:
            return

        self._accumulated_time = 0

        for ent, motion_comp in esper.get_component(MotionComponent.MotionComponent):
            name = esper.component_for_entity(ent, NameTagComponent.NameTagComponent).name

            if name == "shape":
                shape_comp = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
                shape_transform = esper.component_for_entity(ent, TransformComponent.TransformComponent)
                moved_distance = glm.distance(motion_comp.start_position, shape_transform.position)

                if moved_distance >= motion_comp.distance:
                    motion_comp.velocity = -motion_comp.velocity
                    motion_comp.start_position = shape_transform.position
                    continue

                shape_comp.translate(glm.ivec3(int(motion_comp.velocity.x), int(motion_comp.velocity.y), int(motion_comp.velocity.z)))

        pass
