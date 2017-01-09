#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import sys

import plotly
import plotly.graph_objs as go

"""
IB111 Project01
================
Simple game with AI ("Člověče, nezlob se")
Author: František Zatloukal
"""

# Define AIs that you want in game
# Available options: finish_one_by_one, max_on_board, aggressive, smart_ai
PLAYER_AI = ["finish_one_by_one", "max_on_board", "aggressive", "smart_ai"]
BOARD_SIZE = 40

class Player(object):
    """
    Represents single player
    """

    def __init__(self, type, id):
        self.type = type
        self.id = id

    # AI Functions begin
    def finish_one_by_one(self, players_houses, battlefield, roll):
        """
        Simple AI
        Will deploy only up to one
        """
        i = 0
        battlefield_field = ""
        our_position = -1
        return_arr = [0, 0, 0]
        for (i, battlefield_field) in enumerate(battlefield):
            if battlefield_field == self.id:
                our_position = i

        if our_position != -1:
            return_arr = [1, our_position, our_position + roll]
            return return_arr
        elif roll == 6:
            return_arr = [0, 0, 0]
            return return_arr
        else:
            return_arr[0] = [-1, 0, 0]
            return return_arr

    def max_on_board(self, players_houses, battlefield, roll):
        """
        Deploys new characteres when possible
        """
        our_positions = [-1]
        return_arr = [0, 0, 0]
        for (i, battlefield_field) in enumerate(battlefield):
            if battlefield_field == self.id:
                our_positions.append(i)

        if roll == 6:
            if 0 not in our_positions:
                if players_houses[self.id] > 0:
                    return_arr = [0, 0, 0]
                    return return_arr
        if 0 in our_positions:
            if roll not in our_positions:
                return_arr = [1, 0, roll]
                return return_arr

        if len(our_positions) > 1:
            return_arr = [1, max(our_positions), max(our_positions) + roll]
            return return_arr
        else:
            return_arr = [-1, 0, 0]
            return return_arr

    def aggressive(self, players_houses, battlefield, roll):
        """
        Deploys when possible
        Kills when possible
        """
        our_positions = []
        return_arr = [0, 0, 0]
        for (i, battlefield_field) in enumerate(battlefield):
            if battlefield_field == self.id:
                our_positions.append(i)

        for (i, our_position) in enumerate(our_positions):
            if our_position + roll <= BOARD_SIZE:
                if battlefield[our_position + roll] != self.id:
                    if battlefield[our_position + roll] != "-":
                        return_arr = [1, our_position, our_position + roll]
                        return return_arr
        if roll == 6:
            if 0 not in our_positions:
                if players_houses[self.id] > 0:
                    return_arr = [0, 0, 0]
                    return return_arr
        if 0 in our_positions:
            if roll not in our_positions:
                return_arr = [1, 0, roll]
                return return_arr

        if len(our_positions) > 0:
            return_arr = [1, max(our_positions), max(our_positions) + roll]
            return return_arr
        else:
            return_arr = [-1, 0, 0]
            return return_arr

    def smart_ai(self, players_houses, battlefield, roll):
        """
        Deploys new player when has less than 2 on the battlefield and second character is in the second half
        Tries to stay behind enemy players in first three quarters of the battlefield
        Kills when possible
        """
        our_positions = []
        return_arr = [0, 0, 0]
        for (i, battlefield_field) in enumerate(battlefield):
            if battlefield_field == self.id:
                our_positions.append(i)

        for (i, our_position) in enumerate(our_positions):
            if our_position + roll <= BOARD_SIZE:
                if battlefield[our_position + roll] != self.id:
                    if battlefield[our_position + roll] != "-":
                        return_arr = [1, our_position, our_position + roll]
                        return return_arr
        if roll == 6:
            if 0 not in our_positions:
                if players_houses[self.id] > 0:
                    return_arr = [0, 0, 0]
                    return return_arr
        if 0 in our_positions:
            if roll not in our_positions:
                return_arr = [1, 0, roll]
                return return_arr

        if len(our_positions) > 0:
            return_arr = [1, max(our_positions), max(our_positions) + roll]
            return return_arr
        else:
            return_arr = [-1, 0, 0]
            return return_arr


    # AI functions end
    def turn(self, roll):
        if self.type == "finish_one_by_one":
            return self.finish_one_by_one(players_houses, battlefield, roll)
        if self.type == "max_on_board":
            return self.max_on_board(players_houses, battlefield, roll)
        if self.type == "aggressive":
            return self.aggressive(players_houses, battlefield, roll)
        if self.type == "smart_ai":
            return self.smart_ai(players_houses, battlefield, roll)  
            
# Player Class end

def init_battlefield():
    """
    Creates 1D array to store players positions
    """
    battlefield_init = [] #BOARD_SIZE
    i = 0
    while i <= BOARD_SIZE:
        battlefield_init.append("-")
        i += 1
    return battlefield_init

def init_player_houses():
    """
    Initilizes player start buffer
    """
    i = 0
    players_houses_init = []
    while i <= PLAYERS_NUM:
        players_houses_init.append(4)
        i += 1
    return players_houses_init

def init_player_finish():
    """
    Initializes finish houses for each player
    """
    i = 0
    players_finish_init = []
    while i <= PLAYERS_NUM:
        players_finish_init.append([0, 0, 0, 0, 1, 1]) # Fill the end with 1s to signalize over-roll
        i += 1
    return players_finish_init

def roll():
    """
    Random between 1-6
    """
    return random.randint(1, 6)

def turn(player_id, players_houses, players_finish, battlefield, roll):
    """
    array request[int action(-1 = nothing, 0 = deploy, 1 = turn), int initial position, int new position]
    """
    request = [""]

    request = players[player_id].turn(roll)

    print("Player:" + str(player_id))
    print("Rolled ===== " + str(roll))
    print("Request in turn: ", end="")
    if request[0] == -1:
        print("Do nothing")
    if request[0] == 0:
        print("Deploy; Remaining in house: " + str(players_houses[player_id]))
    if request[0] == 1:
        print("Turn")
        print("Initial position: " + str(request[1]) + " ; ", end="")
        if not request[2] > BOARD_SIZE:
            print("New position: " + str(request[2]))
        elif players_finish[player_id][(request[2] - (BOARD_SIZE + 1))] != 0:
            print("Tried to finish but not possible, doing nothing")
        else:
            print("Finish" + "; Remaining in house: " + str(players_houses[player_id]))

    # Do what AI wants
    if request[0] == 0:
        players_houses[player_id] -= 1
        battlefield[0] = player_id
    elif request[0] == 1:
        if request[2] > BOARD_SIZE:
            if players_finish[player_id][(request[2] - (BOARD_SIZE + 1))] == 0:
                battlefield[request[1]] = "-"
        if not request[2] > BOARD_SIZE:
            battlefield[request[1]] = "-"
            if battlefield[request[2]] != "-":
                players_houses[battlefield[request[2]]] += 1
            battlefield[request[2]] = player_id
        return 0

def game_status_refresh(player_id, players_houses, battlefield):
    """
    Checks if there is winner
    0 = game is over, we have a winner!
    1 = game is running
    """
    for battlefield_field in enumerate(battlefield):
        if battlefield_field == player_id:
            return 1
    if players_houses[player_id] == 0:
        return 0

print("pr01.py starting...")

PLAYERS_NUM = len(PLAYER_AI)
player_victories = []

chart_run = 0
run_counter = 0
player_id = 0
game_status = 1

i = 0
players = []

while i != len(PLAYER_AI):
    players.append(Player(PLAYER_AI[i], i))
    i += 1

if len(sys.argv) > 1:
    # PyChart run requested, using sys.argv[1] as run count
    chart_run = 1
    run_counter = int(sys.argv[1]) - 1
    j = 0
    while j < PLAYERS_NUM:
        player_victories.append(0)
        j += 1

print("Init battlefield...")
battlefield = init_battlefield()
players_finish = init_player_finish()

print("Init players...")
players_houses = init_player_houses()

while game_status != 0:
    while player_id <= PLAYERS_NUM:
        roll_num = roll()
        turn(player_id, players_houses, players_finish, battlefield, roll_num)
        while roll_num == 6:
            roll_num = roll()
            turn(player_id, players_houses, players_finish, battlefield, roll_num)
        for (j, battlefield_field_preview) in enumerate(battlefield):
            print(battlefield_field_preview, end="")
        print("")
        game_status = game_status_refresh(player_id, players_houses, battlefield)
        if game_status == 0:
            print("Player " + str(player_id) + " won")
            if run_counter != 0 and chart_run == 1:
                # End of actual pass, reinit variables and run again
                game_status = 1
                print("Reinit battlefield...")
                battlefield = init_battlefield()
                players_finish = init_player_finish()
                print("Reinit players...")
                players_houses = init_player_houses()
                run_counter -= 1
                print("Run Counter: " + str(run_counter))
                player_victories[player_id] += 1
                print("Victories - " + str(player_victories))
                break
            break
        player_id += 1
        if player_id == PLAYERS_NUM:
            player_id = 0

# Generate graph
if chart_run == 1:
    data = [go.Bar(
        x=['finish_one_by_one', 'max_on_board', 'aggressive', 'smart_ai'],
        y=player_victories
    )]
    plotly.offline.plot(data, filename='basic-bar')
