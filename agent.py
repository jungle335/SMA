from grid import *
import random
from events import *
from agentmessage import *
from inbox import *
from path import * 
from planning import *
"""
N t T W H
nr_MyAgenti
timpul necesar pentru a efectua operatii asupra mediului
timpul total al simularii
latimea grid-ului
inaltimea grid-ului
"""



# Define class Agent, inherits Grid
'''
Contains methods:
    * get_agent_position() - Get current agent's position

    * update_score(nr_points) - Updates score

    * Move(direction) - Returns the new position if position is valid
                      - Direction: North, South, West, East

    * update_agent_position(position) - Updates the agent's position

    * Pick(tile_color) - Pick a tile from the current position

    * Droptile() - Drop a tile on the current position

    * Use_tile(direction) - Use a tile on a hole
                          - Direction must be the direction of the hole

    * holesNeighbours() - Check if there are any holes as neighbours
                        - Returns direction of the hole neighbour if exist, empty string otherwise

    * TransferPoints(Agent, points)

    * perceive(events) - Add perceptions and return an action (currently) a direction)
'''
class Agent(Grid):
    x, y, colour, score = None, None, None, 0
    id = 1
    is_Holding_Tile = None
    plan = None

    def __init__(self, x, y, colour, grid, plan: Plan=None):
        super().__init__(grid.W, grid.H, grid.obstacles, grid.tiles, grid.holes, grid.env)
        self.x = x
        self.y = y
        self.colour = colour
        self.is_Holding_Tile = [False, None]
        self.id = Agent.id
        Agent.id += 1
        self.inbox = Inbox()
        self.plan = plan

    def __str__(self):
        return f"Position: ({self.x}, {self.y})\nColor: {self.colour}"

    def get_agent_score(self):
        return self.score

    def get_agent_position(self):
        return self.x, self.y

    def get_agent_colour(self):
        return self.colour

    def update_score(self, nr_points):
        self.score += nr_points

    # Move towards a specific direction, also checks not to go outside Grid
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
        self.is_Holding_Tile = [True, tile_color]

    # Check if the current position has a group of tiles
    '''
    If current position has already a group of tiles, add them to the stack
    else create a new group to display it on the grid
    '''
    def Droptile(self):
        ag_pos = self.get_agent_position()
        if super().isTile(ag_pos):
            tile_color = self.get_tile_colour(ag_pos)
            print("Going to drop tile with color: " + str(tile_color) + " on a group of tiles.")
            if tile_color == self.is_Holding_Tile[1]:
                tile_key = self.get_key(self.tiles, ag_pos)
                self.tiles[tile_key][0] += 1
        else:
            # Add a new key to tile dictionary to represent it on the visual Grid
            new_tile_key = list(self.tiles.keys())[-1] + 1
            self.tiles[new_tile_key] = [1, self.is_Holding_Tile[1], ag_pos]
            print("Going to drop tile on an empty Grid cell.")
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

        if self.holes[get_hole][0] == 1 and self.holes[get_hole][1] == self.get_agent_colour():
            self.update_score(40)
            print(f"The agent {self.id} gets 40 and has a new number of points {self.get_agent_score()}")
        elif self.holes[get_hole][0] != 1 and self.holes[get_hole][1] == self.get_agent_colour():
            self.update_score(10)
            print(f"The agent {self.id} gets 10 and has a new number of points {self.get_agent_score()}")

        self.holes[get_hole][0] -= 1
        if self.holes[get_hole][0] == 0:
            del self.holes[get_hole]
        self.is_Holding_Tile = [False, None]

    def Transfer_points(self, MyAgent, points):
        print(f"Initial points for agent {self.id} is {self.get_agent_score()}\nInitial points for agent {MyAgent.id} is {MyAgent.get_agent_score()}")
        MyAgent.update_score(points)
        self.update_score(-points)
        print(f"Transfered points from {self.id} to agent {MyAgent.id}\nNow the agent {MyAgent.id} has {MyAgent.get_agent_score()} and {self.id} has {self.get_agent_score()}")

    # Get coming direction at a new position
    def coming_direction(self, direction):
        if direction == "North":
            return "South"
        elif direction == "South":
            return "North"
        elif direction == "West":
            return "East"
        elif direction == "East":
            return "West"

    # Functions that read the perceptions
    def perceive(self, events):
        ag_pos = self.get_agent_position()
        if self.isTile(ag_pos) and not self.is_Holding_Tile[0]:
            return f"Pick: {self.get_tile_colour(ag_pos)}"

        dir_neighs = self.holesNeighbours()
        if dir_neighs != '':
            return f"UseTile: {dir_neighs}"
        
        holesPos = [elem[2] for elem in events.holes.values()]
        if not events.has_Tile[0]:
            pos_list = get_manhattan_dist(events.tiles, ag_pos)
            new_pos = path(self.H, self.W, self.get_agent_position(), pos_list, self.obstacles, holesPos)
     
            next_dr = None
            if new_pos[1] < ag_pos[1]:
                next_dr = "West"
            elif new_pos[1] > ag_pos[1]:
                next_dr = "East"
            elif new_pos[0] < ag_pos[0]:
                next_dr = "North"
            else:
                next_dr = "South"
            
            return f"Move: {next_dr}"

        elif events.has_Tile[0]:
            holesValues = events.holes.values()
            holesColorAndPos = [(elem[1], elem[2]) for elem in holesValues if elem[1] == self.is_Holding_Tile[1]]
            holeKeys = [self.get_key(self.holes, hole[1]) for hole in holesColorAndPos]
            validHoles = {}
            for key in holeKeys:
                validHoles[key] = events.holes[key]
            pos_list = get_manhattan_dist(validHoles, ag_pos)
            new_pos = path(self.H, self.W, self.get_agent_position(), pos_list, events.obstacles)
            
            next_dr = None
            if new_pos[1] < ag_pos[1]:
                next_dr = "West"
            elif new_pos[1] > ag_pos[1]:
                next_dr = "East"
            elif new_pos[0] < ag_pos[0]:
                next_dr = "North"
            else:
                next_dr = "South"
            
            return f'Move: {next_dr}'
 
                 
        # return random.choice(['North', 'South', 'West', 'East'])
    def send_message(self, message):
        for receiver in message.receivers:
            receiver.inbox.add_message(message)

    def receive_message(self):
        msg_list = []
        while len(self.inbox) != 0:
            msg = self.inbox.get_message()
            msg_list.append(msg)
        return msg_list