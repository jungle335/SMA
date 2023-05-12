from environment import *
from grid import *
from agent import *

# Function to read the file:
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

        return MyAgents, Grid(*first_line[-2:], obstacles, tiles_dict, holes_dict,
                                                           Environment(*first_line[:3]))
