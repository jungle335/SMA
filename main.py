import sys
from agent import *
from events import *
import pygame
import os

agents = read_map("./SMA/tests/system__default.txt")

gridW = agents[0].W
gridH = agents[0].H

window = (800, 600)
CELL_SIZE = (window[0] // gridW, window[1] // gridH)
move_timer = 1500

pygame.init()
window = pygame.display.set_mode(window)
matrix = [[0 for _ in range(gridW)] for _ in range(gridH)]
pygame.time.set_timer(pygame.USEREVENT, move_timer)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            for ag in agents:
                print("CURRENT AGENT: " + str(ag.id))
                direction = ag.perceive(Events(ag.holes, ag.tiles, ag.obstacles, [(other_ag.get_agent_position(), other_ag.colour, other_ag.score) \
                                                                for other_ag in agents if ag.id != other_ag.id], ag.is_Holding_Tile))
                # Check if current position is a tile
                if ag.isTile(ag.get_agent_position()) and not ag.is_Holding_Tile[0]:
                    ag.Pick(ag.get_tile_colour(ag.get_agent_position()))
                    ag.update_tiles(ag.get_agent_position())
                # Check if there are holes neighbours
                dir_neighs = ag.holesNeighbours()
                if dir_neighs != '':
                    ag.Use_tile(dir_neighs)

                print("AFTER PERCEPTIONS IT MOVES TO: " + direction)
                new_pos = ag.Move(direction)
                holes_values = ag.holes.values()
                holes_positions = [elem[2] for elem in holes_values]
                print(holes_positions)
                if new_pos not in ag.obstacles and new_pos in holes_positions or new_pos not in holes_positions and new_pos in ag.obstacles or new_pos in ag.obstacles and new_pos in holes_positions:
                    print("not ok")
                else:
                    
                    ag.update_agent_position(new_pos)
                print("Agent will move from position: ", ag.get_agent_position(), "To position: ", new_pos)
                

                # ag.perceive(Events(ag.))
                

                # new_pos = ag.Move(direction, ag.W, ag.H)
                # neigh_hole_direction = ag.holesNeighbours()
                # if neigh_hole_direction != '':
                #     print("where to hole", neigh_hole_direction)
                #     ag.Use_tile(neigh_hole_direction)
                # print(ag.holes)
                # if new_pos in ag.obstacles or new_pos in [elem[2] for elem in ag.holes.values()]:
                #     direction = random.choice(["North", "South", "East", "West"])
                #     print("test apel")
                #     if ag.is_Holding_Tile[0]:
                #         ag.Droptile()
                # else:
                #     ag.update_agent_position(new_pos)   

    window.fill((255, 255, 255))

    for row in range(gridW):
        for col in range(gridH):
            rect = pygame.Rect(row * CELL_SIZE[0], col * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1])
            pygame.draw.rect(window, (0, 0, 0), rect, 1)

            for ag in agents:
                if (row, col) == ag.get_agent_position():
                    font = pygame.font.SysFont(None, 40)
                    text = font.render(f"Ag {ag.id} " + ag.colour[:2].upper(), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] / 2))
                    window.blit(text, text_rect)

                if (row, col) in ag.obstacles:
                    pygame.draw.line(window, (255, 0, 0), (col*CELL_SIZE[0], row*CELL_SIZE[1]), ((col+1)*CELL_SIZE[0], (row+1)*CELL_SIZE[1]), 3)
                    pygame.draw.line(window, (255, 0, 0), ((col+1)*CELL_SIZE[0], row*CELL_SIZE[1]), (col*CELL_SIZE[0], (row+1)*CELL_SIZE[1]), 3)

                for key in ag.tiles:
                    if (row, col) == ag.tiles[key][2]:
                        font = pygame.font.SysFont(None, 40)
                        text = font.render("T" + str(ag.tiles[key][0]) + ag.tiles[key][1][:2].upper(), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] / 2))
                        window.blit(text, text_rect)

                for key in ag.holes:
                    if (row, col) == ag.holes[key][2]:
                        font = pygame.font.SysFont(None, 40)
                        text = font.render("H" + str(ag.holes[key][0]) + ag.holes[key][1][:2].upper(), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] / 2))
                        window.blit(text, text_rect)

    pygame.display.update()
