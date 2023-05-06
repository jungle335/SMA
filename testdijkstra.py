import numpy as np


def dijkstra(start, end, obstacles):
    # Set up the grid dimensions
    x_min = min(start[0], end[0], *[obs[0] for obs in obstacles])
    x_max = max(start[0], end[0], *[obs[0] for obs in obstacles])
    y_min = min(start[1], end[1], *[obs[1] for obs in obstacles])
    y_max = max(start[1], end[1], *[obs[1] for obs in obstacles])
    n = x_max - x_min + 1
    m = y_max - y_min + 1
    print(x_min, x_max, y_min, y_max)
    print(n, m)
    # Create the grid
    grid = np.ones((4, 4))
    for obs in obstacles:
        grid[obs[0]][obs[1]] = np.inf
    
    print(grid)
    # Apply Dijkstra's algorithm
    distance = np.ones((n, m)) * np.inf
    visited = np.zeros((n, m), dtype=bool)
    distance[start[0] - x_min][start[1] - y_min] = 0
    while not visited[end[0] - x_min][end[1] - y_min]:
        x, y = np.unravel_index(np.argmin(distance), distance.shape)
        visited[x][y] = True
        if x > 0 and not visited[x-1][y]:
            distance[x-1][y] = min(distance[x-1][y], distance[x][y] + grid[x-1][y])
        if x < n-1 and not visited[x+1][y]:
            distance[x+1][y] = min(distance[x+1][y], distance[x][y] + grid[x+1][y])
        if y > 0 and not visited[x][y-1]:
            distance[x][y-1] = min(distance[x][y-1], distance[x][y] + grid[x][y-1])
        if y < m-1 and not visited[x][y+1]:
            distance[x][y+1] = min(distance[x][y+1], distance[x][y] + grid[x][y+1])

    # Backtrack from end to start to get the shortest path
    path = [(end[0] - x_min, end[1] - y_min)]
    while path[-1] != (start[0] - x_min, start[1] - y_min):
        x, y = path[-1]
        if x > 0 and distance[x-1][y] < distance[x][y]:
            path.append((x-1, y))
        elif x < n-1 and distance[x+1][y] < distance[x][y]:
            path.append((x+1, y))
        elif y > 0 and distance[x][y-1] < distance[x][y]:
            path.append((x, y-1))
        elif y < m-1 and distance[x][y+1] < distance[x][y]:
            path.append((x, y+1))
    
    # Convert path coordinates to original grid coordinates
    path = [(x + x_min, y + y_min) for x, y in path[::-1]]
    return path

print(dijkstra((3, 2), (1, 2), [(2,2), (2,1), (1,1)]))
