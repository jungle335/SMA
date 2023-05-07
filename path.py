import numpy as np
import heapq

# Compute Manhattan Distance to the nearest objective (Tile or Hole)
def get_manhattan_dist(dictionary, ag_pos):
    positions = [val[2] for val in dictionary.values()]
    positions =  sorted(positions, key=lambda pos: abs(ag_pos[0] - pos[0]) + abs(ag_pos[1] - pos[1]))
    if len(positions) > 0:
        return positions[0]
    else:
        return ag_pos


def path(n,m, start, end, obstacles, holes = []):
    num_rows = n
    num_cols = m
    grid = np.ones((n, m))

    for obs in obstacles:
        grid[obs[0]][obs[1]] = np.inf
    
    for hole in holes:
        grid[hole[0]][hole[1]] = np.inf

    graph = [[] for _ in range(num_rows * num_cols)]
    for i in range(num_rows):
        for j in range(num_cols):
            if j > 0:
                graph[i*num_cols + j].append((i*num_cols + j - 1, grid[i][j-1]))
            if j < num_cols - 1:
                graph[i*num_cols + j].append((i*num_cols + j + 1, grid[i][j+1]))
            if i > 0:
                graph[i*num_cols + j].append(((i-1)*num_cols + j, grid[i-1][j]))
            if i < num_rows - 1:
                graph[i*num_cols + j].append(((i+1)*num_cols + j, grid[i+1][j]))

    start_node = start[0] * num_cols + start[1]
    end_node = end[0] * num_cols + end[1]

    dist = [np.inf for _ in range(num_rows * num_cols)]
    dist[start_node] = 0

    visited = [False for _ in range(num_rows * num_cols)]

    heap = []
    heapq.heappush(heap, (0, start_node))
    while heap:
        (d, u) = heapq.heappop(heap)
        if u == end_node:
            break
        if visited[u]:
            continue
        visited[u] = True

        for (v, w) in graph[u]:
            if not visited[v]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    heapq.heappush(heap, (alt, v))

    path = []
    current_node = end_node
    while current_node != start_node:
        path.append(current_node)
        for (v, w) in graph[current_node]:
            if dist[v] == dist[current_node] - w:
                current_node = v
                break
    path.append(start_node)
    path.reverse()

    path_pos = []
    for node in path[:2]:
        row = node // num_cols
        col = node % num_cols
        path_pos.append((row, col))
    
    if len(path_pos) > 1:
        return path_pos[1]
    else:
        return start
    

