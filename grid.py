from environment import *

# Define Grid class, inherits environment
'''
Containe methods:
    isTile()
    isHole()
    get_tile_color()
    update_tiles()
    get_key()
'''
class Grid(Environment):
    W, H = None, None
    obstacles, tiles, holes = None, None, None
    env = None

    def __init__(self, W, H, obstacles, tiles, holes, env):
        super().__init__(env.N, env.t, env.T)
        self.W = W
        self.H = H
        self.obstacles = obstacles
        self.tiles = tiles
        self.holes = holes
        self.env = env

    def __str__(self):
        env_str = super().__str__()
        return f"{env_str}, \nGrid: W={self.W}, H={self.H}, obstacles={self.obstacles}, tiles={self.tiles}, holes={self.holes}"

    def isTile(self, position):
        return position in [elem[2] for elem in self.tiles.values()]

    def isHole(self, position):
        return position in [elem[2] for elem in self.holes.values()]

    def get_tile_colour(self, position):
        print(position)
        print([elem[1] for elem in self.tiles.values() if position == elem[2]])
        return [elem[1] for elem in self.tiles.values() if position == elem[2]][0]

    def update_tiles(self, position):
        for key in list(self.tiles.keys()):
            if position in self.tiles[key]:
                self.tiles[key][0] -= 1
                if self.tiles[key][0] == 0:
                    del self.tiles[key]
                    break

    def get_key(self, dictionary, position):
        for key, value in dictionary.items():
            if value[2] == position:
                return key
        return None