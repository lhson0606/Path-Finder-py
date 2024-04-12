import esper

import Source.Algorithm.VisualizedAlgorithm as VisualizedAlgorithm
import Source.App as App

class VisualizingProcessor(esper.Processor):

    def __init__(self):
        self._algorithm = None
        self._is_enabled = False
        pass

    def enable(self, alg: VisualizedAlgorithm):
        self._is_enabled = True
        self._algorithm = alg
        pass

    def disable(self):
        self._algorithm.clean_up()
        self._is_enabled = False
        pass

    def process(self, dt):
        if not self._is_enabled:
            return

        self._algorithm.solve_and_visualize()

        pass
