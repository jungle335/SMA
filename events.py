import pade

class Events:
    holes, tiles, obstacles = None, None, None
    ag_positions = None
    has_Tile = None
    score = None
   
    def __init__(self, holes, tiles, obstacles, ag_positions, has_Tile, score = None):
        self.holes = holes
        self.tiles = tiles
        self.obstacles = obstacles
        self.ag_positions = ag_positions
        self.has_Tile = has_Tile
        self.score = score

    def __str__(self):
        return f"Holes: {self.holes}, \nTiles: {self.tiles}, \nObstacles: {self.obstacles}, \nAgent Positions: {self.ag_positions}, \nHas_Tile: {self.has_Tile}\n"

# Define the message format
