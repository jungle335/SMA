import sys
from agent import *
from events import *
from read_map import *
import pygame
import os

# Call function to read the file
agents, grid = read_map("./tests/system__default.txt")

# Get Width and Height and scale the Grid Window to fit
gridW = agents[0].W
gridH = agents[0].H

window = (800, 600)
CELL_SIZE = (window[0] // gridW, window[1] // gridH)
move_timer = 1500#grid.t

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
            # Iterate through all available agents
            for ag in agents:
                if len(ag.holes) == 0:
                    print("System ended")
                    pygame.quit()
                    sys.exit()

                print("\n* CURRENT AGENT: " + str(ag.id))


                action = ag.perceive(Events(ag.holes, ag.tiles, ag.obstacles, [(other_ag.get_agent_position(), other_ag.colour, other_ag.score) \
                                                                for other_ag in agents if ag.id != other_ag.id], ag.is_Holding_Tile))
                ag.plan.add_Action(action)

                messagedActions = []
                if len(ag.plan.actions) != 0:
                    for other_ag in agents:
                        if ag.id != other_ag.id:
                            message_content = Message(agPosition=ag.get_agent_position(), agNextAction=ag.plan.actions[0] ,agHoldingTileColor=ag.is_Holding_Tile[1])
                            message = AgentMessage(conversation_id=str(ag.id) + ":" + str(other_ag.id))
                            message.setSender(ag)
                            message.addReceivers(other_ag)
                            message.addContent(message_content)
                            ag.send_message(message)
                            if len(ag.ongoingConv) != 0 and [message.conversation_id, True] in ag.ongoingConv:
                                convIndex = ag.ongoingConv.index([message.conversation_id, True])
                                while ag.ongoingConv[convIndex][1]:
                                    messagedActions.append(ag.request_reply(other_ag))
                                    ag.end_conversation(convIndex)
                print(messagedActions)
                ag.plan.add_Action(messagedActions[0])

                print(f"Plans for the 'Agent {ag.id}':")
                while len(ag.plan.actions) != 0:
                    print(ag.plan.actions)
                    if ":" in ag.plan.actions[0]:
                        get_action_name, get_action_params = ag.plan.actions[0].split(": ")
                    else:
                        get_action_name = ag.plan.actions[0]

                    if get_action_name == "Move":
                            new_pos = ag.Move(get_action_params)
                            # Check if the new position is blocked by obstacle or by hole
                            # change position if is clear
                            holes_values = ag.holes.values()
                            holes_positions = [elem[2] for elem in holes_values]
                            if (new_pos not in ag.obstacles and new_pos in holes_positions) or (new_pos not in holes_positions and new_pos in ag.obstacles) or (new_pos in ag.obstacles and new_pos in holes_positions):
                                print("* Agent will keep the current position this step!")
                            else:
                                print("* Agent will move from position: ", ag.get_agent_position(), "To position: ", new_pos)
                                ag.update_agent_position(new_pos)

                    if get_action_name == "Pick":
                        ag.Pick(get_action_params)
                        ag.update_tiles(ag.get_agent_position())
                    
                    if get_action_name == "UseTile":
                        points_to_be_transfered = 5
                        ag.Use_tile(get_action_params)
                        if points_to_be_transfered < ag.get_agent_score():
                            ag.Transfer_points([other_ag for other_ag in agents if ag.id != other_ag.id][0], 5)

                    if get_action_name == "DoNothingTestAction":
                        print("*****DOES NOTHING: This is only for test and does nothing!")

                    ag.plan.remove()


                print("\n")

# Draw the Visual Grid
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
