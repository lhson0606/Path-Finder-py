import Source.Algorithm.VisualizedAlgorithm as VisualizedAlgorithm

import queue
import glm
import Source.Map.Map as Map


def h(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


def d(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


class VisualizedDijkstra(VisualizedAlgorithm.VisualizedAlgorithm):
    def get_cost(self, start: glm.ivec3, goal: glm.ivec3):
        if start == goal:
            return 0

        open_set = queue.Queue()
        came_from = {}

        g_score = {start: 0}
        open_set.put(start)

        while not open_set.empty():
            current = open_set.get()

            if current == goal:
                return g_score[current]

            for neighbor in self.map.get_neighbors(current):
                tentative_g_score = g_score[current] + d(glm.vec3(current), glm.vec3(neighbor))
                current_score = g_score[neighbor] if neighbor in g_score.keys() else float("inf")
                if tentative_g_score < current_score:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score

                    if neighbor not in open_set.queue:
                        open_set.put(neighbor)

        return float("inf")
        pass

    def find_path(self, start: glm.ivec3, goal: glm.ivec3):
        return self.dijkstra_search(start, goal, self.map)
        pass

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def dijkstra_search(self, start: glm.ivec3, goal: glm.ivec3, m: Map):
        open_set = queue.Queue()
        came_from = {}

        g_score = {start: 0}
        open_set.put(start)

        while not open_set.empty():
            self.search_volume += 1
            current = open_set.get()

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in m.get_neighbors(current):
                tentative_g_score = g_score[current] + d(glm.vec3(current), glm.vec3(neighbor))
                current_score = g_score[neighbor] if neighbor in g_score.keys() else float("inf")
                if tentative_g_score < current_score:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score

                    if neighbor not in open_set.queue:
                        open_set.put(neighbor)

        return None
