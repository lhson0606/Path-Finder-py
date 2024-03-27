import glm
import heapq


# reference: https://en.wikipedia.org/wiki/A*_search_algorithm

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def get_neighbors(current):
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if i == 0 and j == 0 and k == 0:
                    continue
                neighbors.append(glm.ivec3(current.x + i, current.y + j, current.z + k))

    return neighbors


def h(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


def d(a: glm.vec3, b: glm.vec3):
    return glm.distance(a, b)


def a_star_search(start: glm.ivec3, goal: glm.ivec3):
    open_set = [(0, start)]
    came_from = {}

    g_score = {start: 0}

    f_score = {start: h(glm.vec3(start), glm.vec3(goal))}

    while len(open_set) > 0:
        current = open_set[0][1]

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.pop(0)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + d(glm.vec3(current), glm.vec3(neighbor))
            if neighbor not in g_score.keys() or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(glm.vec3(neighbor), glm.vec3(goal))

                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None
