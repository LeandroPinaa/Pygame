from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

# 1. creating matrix and grid
matrix = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]]
grid = Grid(matrix=matrix)

# 2. creating start and end cell
start = grid.node(0, 0)
end = grid.node(5, 2)

# 3. create a finder with a movement style
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)  # caso eu queira diagonal faço isso

# 4. use the finder to find the path
path, runs = finder.find_path(start, end, grid)
# path vai ser uma lista com todas as coordenadas do menor caminho possível até o fim :)
print(path)

