import Source.Algorithm.VisualizedAlgorithm as VisualizedAlgorithm

import heapq
import glm
import Source.Map.Map as Map


def h(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


def d(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


class VisualizedAStar(VisualizedAlgorithm.VisualizedAlgorithm):
    def get_cost(self, start: glm.ivec3, goal: glm.ivec3):
        if start == goal:
            return 0

        open_set = [(0, start)]
        came_from = {}

        g_score = {start: 0}

        f_score = {start: h(glm.vec3(start), glm.vec3(goal))}

        while len(open_set) > 0:
            current = open_set[0][1]

            if current == goal:
                return g_score[current]

            open_set.pop(0)
            for neighbor in self.map.get_neighbors(current):
                tentative_g_score = g_score[current] + d(glm.vec3(current), glm.vec3(neighbor))
                if neighbor not in g_score.keys() or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + h(glm.vec3(neighbor), glm.vec3(goal))

                    if neighbor not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return float("inf")
        pass

    def find_path(self, start: glm.ivec3, goal: glm.ivec3):
        return self.a_star_search(start, goal, self.map)
        pass

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def a_star_search(self, start: glm.ivec3, goal: glm.ivec3, m: Map):
        open_set = [(0, start)]
        came_from = {}

        g_score = {start: 0}

        f_score = {start: h(glm.vec3(start), glm.vec3(goal))}

        while len(open_set) > 0:
            self.search_volume += 1
            current = open_set[0][1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.pop(0)
            for neighbor in self.map.get_neighbors(current):
                tentative_g_score = g_score[current] + d(glm.vec3(current), glm.vec3(neighbor))
                if neighbor not in g_score.keys() or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + h(glm.vec3(neighbor), glm.vec3(goal))

                    if neighbor not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None
