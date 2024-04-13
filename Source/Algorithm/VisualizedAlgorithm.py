import esper

import Source.Map.Map as Map
import Source.App as App
from abc import ABC, abstractmethod
import Source.ECS.Component.PathComponent as PathComponent
import Source.Manager.ShaderManager as ShaderManager
import Source.ECS.Component.RenderComponent as RenderComponent
from itertools import chain, combinations
import glm
import Source.Util.dy as dy
import time

def unique_list(input_list):
    return list(dict.fromkeys(input_list))


# ref: https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_subset(S, k):
    return list(combinations(S, k))


if "__main__" == __name__:
    print(list(powerset([1, 2, 3])))
    for s in range(0, 3):
        print(str(combinations(range(0, 3), s)))


# ref: https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
# an abstract class that represents a visualized solving Traveling Salesman Problem algorithm
class VisualizedAlgorithm(ABC):
    def __init__(self, m: Map, app: App):
        self.map = m
        self.app = app
        self.path_ent = esper.create_entity(PathComponent.PathComponent(app))
        self._g = {}
        self._p = {}

        shader = self.app.shader_manager.get_shader(ShaderManager.ShaderType.PATH_POINT_SHADER)
        render_comp = RenderComponent.RenderComponent(ShaderManager.ShaderType.PATH_POINT_SHADER, shader)

        esper.add_component(self.path_ent, render_comp)
        self.vertices = []
        self.vertices.append(self.map.start)
        for x in self.map.passing_point_positions:
            self.vertices.append(x)
        self.vertices.append(self.map.goal)
        self.adjacency_matrix = None
        self.time_elapsed = 0
        self.path_length = 0

    @abstractmethod
    def find_path(self, start: glm.ivec3, goal: glm.ivec3):
        pass

    @abstractmethod
    def get_cost(self, start: glm.ivec3, goal: glm.ivec3):
        pass

    def build_adjacency_matrix(self):
        adj_matrix = {}
        for x in range(len(self.vertices)):
            adj_matrix[x] = {}
            for y in range(len(self.vertices)):
                adj_matrix[x][y] = self.get_cost(self.vertices[x], self.vertices[y])
        return adj_matrix

    def solve_and_visualize(self):

        self.adjacency_matrix = self.build_adjacency_matrix()

        path_comp = esper.component_for_entity(self.path_ent, PathComponent.PathComponent)

        self.path_length = 0
        start_time = time.time()

        self._g = {}
        self._p = {}

        if len(self.map.passing_point_positions) > 0:
            positions = self.solve_TSP(self.map.goal, len(self.vertices))
        else:
            positions = self.find_path(self.map.start, self.map.goal)
            self.path_length = self.get_cost(self.map.start, self.map.goal)

        end_time = time.time()

        self.time_elapsed = end_time - start_time

        if positions is None:
            raise Exception("No path found")

        path_comp.build_path(positions)

    def solve_TSP(self, goal: glm.ivec3, n):
        for k in range(1, n):
            key = (k, tuple([]))
            self._g[key] = self.adjacency_matrix[0][k]
            self._p[key] = 0

        for s in range(1, n - 1):
            for S in combinations(range(1, n - 1), s):
                for k in range(1, n - 1):
                    if k in S:
                        continue
                    self.__resolve_min(k, S)

        self.__resolve_min(n - 1, tuple(range(1, n - 1)))

        if self._g[(n - 1, tuple(range(1, n - 1)))] == float("inf"):
            return None

        return self.__reconstruct_path()
        pass

    def __reconstruct_path(self):
        order = []
        our_list = list(range(1, len(self.vertices) - 1))
        S = tuple(our_list)
        order.append(len(self.vertices) - 1)
        start = self._p[(len(self.vertices) - 1, S)]

        cur = start
        while len(S) > 0:
            order.append(cur)
            our_list.remove(cur)
            S = tuple(our_list)
            cur = self._p[(cur, S)]

        order.append(0)

        order.reverse()

        # calculate the path length
        for i in range(0, len(order) - 1):
            self.path_length += self.adjacency_matrix[order[i]][order[i + 1]]

        result = []

        for i in range(0, len(order) - 1):
            path_result = self.find_path(
                self.vertices[order[i]],
                self.vertices[order[i + 1]]
            )

            if path_result is None:
                return None

            result.extend(path_result)

        path_result = self.find_path(
            self.vertices[order[len(order) - 1]],
            self.vertices[-1]
        )

        if path_result is None:
            return None

        result.extend(path_result)

        return unique_list(result)
        pass

    def __resolve_min(self, k, subset):
        min_value = float("inf")
        for S in get_subset(subset, len(subset) - 1):
            for x in subset:
                if x in S:
                    continue
                value = self.adjacency_matrix[k][x] + self._g[(x, S)]
                if value < min_value:
                    min_value = value
                    self._p[(k, subset)] = x

        self._g[(k, subset)] = min_value
        pass

    def clean_up(self):
        path_comp = esper.component_for_entity(self.path_ent, PathComponent.PathComponent)
        path_comp.clean_up()
        esper.delete_entity(self.path_ent, True)
        pass
