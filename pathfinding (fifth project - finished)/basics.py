# pathfinding básico pro inimigo seguir, mas trava em obstáculo: (usei no zelda)
# def get_player_distance_direction(self, player):
# enemy_vec = vec(self.rect.center)
# player_vec = vec(player.rect.center)
# distance = (player_vec - enemy_vec).magnitude()  # com magnitude pega a distância de vdd
# if distance > 0:
# direction = (player_vec - enemy_vec).normalize()  # pega a direção
# else:
# direction = vec(0, 0)
# return distance, direction

# novo tipo de pathfinding pelo clear code:

# PRIMEIRO: precisamos de um mapa (claramente) com por ex 1 sendo nada e 0 parede, com as coor do player e target
# SEGUNDO: encontrar o caminho mais curto do target para o player
from pathfinding.core.grid import Grid  # esse grid é uma classe pra fazer o grid
from pathfinding.finder.a_star import AStarFinder  # tipo de busca A* q nem djikstra
from pathfinding.core.diagonal_movement import DiagonalMovement  # classe para permitir movimento diagonal

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
# runs vai ser um nmr de quantas células o finder passou para encontrar o menor caminho possível (meio inútil)
print(path)

