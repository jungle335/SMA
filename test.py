import sys
from agent import *
from events import *
from read_map import *
import pygame
import os
import threading

def updateGrid():
    window.fill((255, 255, 255))
    move_text = 1
    for row in range(gridW):
        for col in range(gridH):
            rect = pygame.Rect(row * CELL_SIZE[0], col * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1])
            pygame.draw.rect(window, (0, 0, 0), rect, 1)

            for ag in agents:
                if (row, col) == ag.get_agent_position():
                    font = pygame.font.SysFont(None, 40)
                    text = font.render(f"Ag {ag.id} " + ag.colour[:2].upper(), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] / 4 * move_text))
                    move_text += 1
                    window.blit(text, text_rect)

                if (row, col) in ag.obstacles:
                    pygame.draw.line(window, (255, 0, 0), (col*CELL_SIZE[0], row*CELL_SIZE[1]), ((col+1)*CELL_SIZE[0], (row+1)*CELL_SIZE[1]), 3)
                    pygame.draw.line(window, (255, 0, 0), ((col+1)*CELL_SIZE[0], row*CELL_SIZE[1]), (col*CELL_SIZE[0], (row+1)*CELL_SIZE[1]), 3)

                for key in ag.tiles:
                    if (row, col) == ag.tiles[key][2]:
                        font = pygame.font.SysFont(None, 40)
                        text = font.render("T" + str(ag.tiles[key][0]) + ag.tiles[key][1][:2].upper(), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] * 3 / 4))
                        window.blit(text, text_rect)

                for key in ag.holes:
                    if (row, col) == ag.holes[key][2]:
                        font = pygame.font.SysFont(None, 40)
                        text = font.render("H" + str(ag.holes[key][0]) + ag.holes[key][1][:2].upper(), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(col * CELL_SIZE[0] + CELL_SIZE[0] / 2, row * CELL_SIZE[1] + CELL_SIZE[1] * 3 / 4))
                        window.blit(text, text_rect)

    pygame.display.update()

def agentAction(ag):
    print("* CURRENT AGENT: " + str(ag.id))
    # Check if there are existing messages for the agent
    msgList = ag.receive_message()
    if len(msgList) != 0:
        for msg in msgList:
            print(f"Received Message from {msg.sender_id}:\n {msg.message}")

    # Build perceptions 
    direction = ag.perceive(Events(ag.holes, ag.tiles, ag.obstacles, [(other_ag.get_agent_position(), other_ag.colour, other_ag.score) \
                                                    for other_ag in agents if ag.id != other_ag.id], ag.is_Holding_Tile))
    
    # Check if current position is a tile in order to pick a tile
    if ag.isTile(ag.get_agent_position()) and not ag.is_Holding_Tile[0]:
        ag.Pick(ag.get_tile_colour(ag.get_agent_position()))
        ag.update_tiles(ag.get_agent_position())

    # Check if there are holes as neighbours in order to use the tile if carrying one
    points_to_be_transfered = 5
    dir_neighs = ag.holesNeighbours()
    if dir_neighs != '':
        ag.Use_tile(dir_neighs)
        if points_to_be_transfered < ag.get_agent_score():
            ag.Transfer_points([other_ag for other_ag in agents if ag.id != other_ag.id][0], 5)

    # Procede to new position
    print("* AFTER PERCEPTIONS IT MOVES TO: " + direction)
    new_pos = ag.Move(direction)
    # Check if the new position is blocked by obstacle or by hole
    # change position if is clear
    holes_values = ag.holes.values()
    holes_positions = [elem[2] for elem in holes_values]
    if (new_pos not in ag.obstacles and new_pos in holes_positions) or (new_pos not in holes_positions and new_pos in ag.obstacles) or (new_pos in ag.obstacles and new_pos in holes_positions):
        print("* Agent will keep the current position this step!")
    else:
        print("* Agent will move from position: ", ag.get_agent_position(), "To position: ", new_pos)
        ag.update_agent_position(new_pos)
    
    # Prepare the messsage to send to other agents
    message_content = Message(agPosition=ag.get_agent_position(), agHoldingTileColor=ag.is_Holding_Tile[1])
    message = AgentMessage(conversation_id="Inform")
    message.setSender(ag.id)
    message.addReceivers([other_ag for other_ag in agents if ag.id != other_ag.id])
    message.addContent(message_content)
    ag.send_message(message)







# Call function to read the file
agents, grid = read_map("./tests/system__default.txt")

# Get Width and Height and scale the Grid Window to fit
gridW = agents[0].W
gridH = agents[0].H

window = (800, 600)
CELL_SIZE = (window[0] // gridW, window[1] // gridH)
move_timer = 1500

pygame.init()
window = pygame.display.set_mode(window)
matrix = [[0 for _ in range(gridW)] for _ in range(gridH)]
pygame.time.set_timer(pygame.USEREVENT, move_timer)

# This represents the step and visual grid generation
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if len(grid.holes) == 0:
                    print("System ended")
                    pygame.quit()
                    sys.exit()
            # Create a list to store the threads for each agent action
            threads = []
            for ag in agents:
                thread = threading.Thread(target=agentAction, args=(ag,))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            
                print("\n")

# Draw the Visual Grid
    updateGrid()
