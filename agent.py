from grid import *
import random
from events import *

"""
N t T W H
nr_MyAgenti
timpul necesar pentru a efectua operatii asupra mediului
timpul total al simularii
latimea grid-ului
inaltimea grid-ului
"""



# Define class Agend, inherits Grid
'''
Contains methods:
    get_agent_position() - Get current agent's position

    update_score(nr_points) - Updates score

    Move(direction) - Returns the new position if position is valid
                    - Direction: North, South, West, East

    update_agent_position(position) - Updates the agent's position

    Pick(tile_color) - Pick a tile from the current position

    Droptile() - Drop a tile on the current position

    Use_tile(direction) - Use a tile on a hole
                        - Direction must be the direction of the hole

    holesNeighbours() - Check if there are any holes as neighbours

    TransferPoints(Agent, points)

    perceive(events) - add perceptions and return an action (currently) a direction)
'''
class Agent(Grid):
    x, y, colour, score = None, None, None, 0
    id = 1
    is_Holding_Tile = None
    host = 'localhost'
    port = 1234

    def __init__(self, x, y, colour, grid):
        super().__init__(grid.W, grid.H, grid.obstacles, grid.tiles, grid.holes, grid.env)
        self.x = x
        self.y = y
        self.colour = colour
        self.is_Holding_Tile = [False, None]
        self.id = Agent.id
        Agent.id += 1

    def __str__(self):
        return f"Position: ({self.x}, {self.y})\nColor: {self.colour}"

    def get_agent_position(self):
        return self.x, self.y

    def update_score(self, nr_points):
        self.score += nr_points

    def Move(self, direction):
        h, w = self.H, self.W
        if direction == 'North':
            return (self.x - 1, self.y) if 0 <= self.x - 1 < h and 0 <= self.y < w else (self.x, self.y)
        elif direction == 'South':
            return (self.x + 1, self.y) if 0 <= self.x + 1 < h and 0 <= self.y < w else (self.x, self.y)
        elif direction == 'East':
            return (self.x, self.y + 1) if 0 <= self.x < h and 0 <= self.y + 1 < w else (self.x, self.y)
        elif direction == 'West':
            return (self.x, self.y - 1) if 0 <= self.x < h and 0 <= self.y - 1 < w else (self.x, self.y)
        else:
            raise ValueError("The direction should be one of North, South, East, West")

    def update_agent_position(self, position):
        self.x = position[0]
        self.y = position[1]

    def Pick(self, tile_color):
        print(tile_color)
        self.is_Holding_Tile = [True, tile_color]

    def Droptile(self):
        ag_pos = self.get_agent_position()
        if super().isTile(ag_pos):
            tile_color = self.get_tile_colour(ag_pos)
            print("Going to drop tile with color: " + str(tile_color) + " on a group of tiles.")
            if tile_color == self.is_Holding_Tile[1]:
                tile_key = self.get_key(self.tiles, ag_pos)
                self.tiles[tile_key][0] += 1
        else:
            # Adaugam in dictionar un nou key
            new_tile_key = list(self.tiles.keys())[-1] + 1
            self.tiles[new_tile_key] = [1, self.is_Holding_Tile[1], ag_pos]
            print("Going to drop tile on an empty grid cell.")
            self.is_Holding_Tile = [False, None]

    def holesNeighbours(self):
        if self.is_Holding_Tile[0]:
            ag_pos = self.get_agent_position()
            north, south, west, east = (ag_pos[0] + 1, ag_pos[1]), (ag_pos[0] - 1, ag_pos[1]), (
                ag_pos[0], ag_pos[1] - 1), (ag_pos[0], ag_pos[1] + 1)

            holes_values = self.holes.values()
            holes_pos = [elem for elem in holes_values] if len(holes_values) > 0 else []

            for hol_pos in holes_pos:
                if self.is_Holding_Tile[1] == hol_pos[1]:
                    if north == hol_pos[2]:
                        return "North"
                    elif south == hol_pos[2]:
                        return "South"
                    elif west == hol_pos[2]:
                        return "West"
                    elif east == hol_pos[2]:
                        return "East"
            return ""
        return ""

    def Use_tile(self, direction):
        ag_pos = self.get_agent_position()
        hol_pos = None

        if direction == "North":
            hol_pos = (ag_pos[0] + 1, ag_pos[1])
        elif direction == "South":
            hol_pos = (ag_pos[0] - 1, ag_pos[1])
        elif direction == "West":
            hol_pos = (ag_pos[0], ag_pos[1] - 1)
        elif direction == "East":
            hol_pos = (ag_pos[0], ag_pos[1] + 1)

        get_hole = super().get_key(self.holes, hol_pos)
        self.holes[get_hole][0] -= 1
        if self.holes[get_hole][0] == 0:
            del self.holes[get_hole]
        self.is_Holding_Tile = [False, None]

    def Transfer_points(self, MyAgent, points):
        pass

    def get_manhattan_dist(self, dictionary, ag_pos):
        positions = [val[2] for val in dictionary.values()]
        return sorted(positions, key=lambda pos: abs(ag_pos[0] - pos[0]) + abs(ag_pos[1] - pos[1]))

    def coming_direction(self, direction):
        if direction == "North":
            return "South"
        elif direction == "South":
            return "North"
        elif direction == "West":
            return "East"
        elif direction == "East":
            return "West"

    def is_Valid(self, position, direction):
        if position in self.obstacles or position in [elem[2] for elem in self.holes.values()]:
            return False
        else:
            north, south, west, east = (position[0] + 1, position[1]), (position[0] - 1, position[1]), (
                position[0], position[1] - 1), (position[0], position[1] + 1)
            coming_from = self.coming_direction(direction)
            valid_pos = {el: True for el in ['North', 'South', 'West', 'East']}

            if not self.is_Holding_Tile[0]:
                if north in self.obstacles or north in [elem[2] for elem in self.holes.values()] or not (
                        north[0] - 1 >= 0 and north[0] - 1 < self.H and north[1] >= 0 and north[1] < self.W):
                    valid_pos['North'] = False
                if south in self.obstacles or south in [elem[2] for elem in self.holes.values()] or not (
                        south[0] + 1 >= 0 and south[0] + 1 < self.H and south[0] >= 0 and south[0] < self.W):
                    valid_pos['South'] = False
                if west in self.obstacles or west in [elem[2] for elem in self.holes.values()] or not (
                        west[0] >= 0 and west[0] < self.H and west[1] - 1 >= 0 and west[1] - 1 < self.W):
                    valid_pos['West'] = False
                if east in self.obstacles or east in [elem[2] for elem in self.holes.values()] or not (
                        east[0] >= 0 and east[0] < self.H and east[0] + 1 >= 0 and east[0] + 1 < self.W):
                    valid_pos['East'] = False
            else:
                if north in self.obstacles or not (
                        north[0] - 1 >= 0 and north[0] - 1 < self.H and north[1] >= 0 and north[1] < self.W):
                    valid_pos['North'] = False
                if south in self.obstacles or not (
                        0 <= south[0] + 1 < self.H and 0 <= south[0] < self.W):
                    valid_pos['South'] = False
                if west in self.obstacles or not (
                        west[0] >= 0 and west[0] < self.H and west[1] - 1 >= 0 and west[1] - 1 < self.W):
                    valid_pos['West'] = False
                if east in self.obstacles or not (
                        east[0] >= 0 and east[0] < self.H and east[0] + 1 >= 0 and east[0] + 1 < self.W):
                    valid_pos['East'] = False

            valid_pos = {k: v for k, v in valid_pos.items() if k != coming_from}
            return False if all(val == False for val in valid_pos.values()) else True

    def perceive(self, events):
        ag_pos = self.get_agent_position()
        if not events.has_Tile[0]:
            pos_list = self.get_manhattan_dist(events.tiles, ag_pos)
            print(pos_list)
            i = 0
            while i < len(pos_list):
                next_dr = None
                if pos_list[i][1] < ag_pos[1]:
                    next_dr = "West"
                elif pos_list[i][1] > ag_pos[1]:
                    next_dr = "East"
                elif pos_list[i][0] < ag_pos[0]:
                    next_dr = "North"
                else:
                    next_dr = "South"
                if self.is_Valid(self.Move(next_dr), next_dr):
                    return next_dr

                i += 1
        elif events.has_Tile[0]:
            holes_values = events.holes.values()
            holesColorAndPos = [(elem[1], elem[2]) for elem in holes_values]
            print(holesColorAndPos)
            pos_list = self.get_manhattan_dist(events.holes, ag_pos)
            print(pos_list)
            i = 0
            while i < len(pos_list):
                next_dr = None
                if pos_list[i][1] < ag_pos[1]:
                    next_dr = "West"
                elif pos_list[i][1] > ag_pos[1]:
                    next_dr = "East"
                elif pos_list[i][0] < ag_pos[0]:
                    next_dr = "North"
                else:
                    next_dr = "South"
                if self.is_Valid(self.Move(next_dr), next_dr):
                    return next_dr
                i += 1
        return random.choice(['North', 'South', 'West', 'East'])

    

def read_map(filepath):
    MyAgents = []

    with open(filepath) as f:
        # board coordinates
        first_line = [int(x) for x in f.readline().split()]
        f.readline()

        # colors of the MyAgents
        MyAgent_colors = [x for x in f.readline().split()]
        local_ag_pos = f.readline().split()
        MyAgent_pos = [(int(local_ag_pos[i]), int(local_ag_pos[i + 1])) for i in range(0, len(local_ag_pos), 2)]

        # OBSTACLES
        obstacles = []
        while True:
            line = f.readline().strip()
            if line.startswith('TILES') or len(obstacles):
                break
            if line.isspace() or line.startswith('OBSTACLES'):
                continue
            line = line.split()
            obstacles = [(int(line[i]), int(line[i + 1])) for i in range(0, len(line), 2)]

        f.readline()
        tiles_dict, holes_dict = {}, {}
        temp_line, i = f.readline(), 0
        while temp_line.strip() != '':
            cur_line = [int(elem) if elem.isnumeric() else elem for elem in temp_line.split()]
            tiles_dict[i] = cur_line[:-2] + [tuple(cur_line[-2:])]
            temp_line = f.readline()
            i += 1

        f.readline()
        temp_line, i = f.readline(), 0
        while temp_line.strip() != '':
            cur_line = [int(elem) if elem.isnumeric() else elem for elem in temp_line.split()]
            holes_dict[i] = cur_line[:-2] + [tuple(cur_line[-2:])]
            temp_line = f.readline()
            i += 1

        f.close()

        for colour, (x, y) in zip(MyAgent_colors, MyAgent_pos):
            MyAgents.append(
                Agent(x=x, y=y, colour=colour, grid=Grid(*first_line[-2:], obstacles, tiles_dict, holes_dict,
                                                           Environment(*first_line[:3]))))

        return MyAgents
