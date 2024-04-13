import esper

import Source.Algorithm.VisualizedAlgorithm as VisualizedAlgorithm
import Source.App as App
import Source.App.Editor as Editor

class VisualizingProcessor(esper.Processor):

    def __init__(self):
        self._algorithm = None
        self._is_enabled = False
        self._editor = None
        self._elapsed_time = 0
        pass

    def enable(self, alg: VisualizedAlgorithm, editor: Editor.Editor):
        self._is_enabled = True
        self._algorithm = alg
        self._editor = editor
        self._elapsed_time = 0
        pass

    def disable(self):
        self._algorithm.clean_up()
        self._is_enabled = False
        pass

    def process(self, dt):
        if not self._is_enabled:
            return

        # self._algorithm.solve_and_visualize()
        try:
            self._algorithm.solve_and_visualize()
            self._elapsed_time += self._algorithm.time_elapsed
        except Exception as e:
            self._editor.handle_when_no_path_found()

        pass

    def get_elapsed_time(self):
        return self._elapsed_time
        pass
