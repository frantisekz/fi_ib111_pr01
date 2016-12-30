#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IB111 Project01
================
Simple game with AI ("Člověče, nezlob se")
Author: František Zatloukal

"""

import random
import sys

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

# AI Functions begin
def finish_one_by_one(player_id, players_houses, battlefield, roll):
    # stupid AI
    i = 0
    battlefield_field = ""
    our_position = -1
    return_arr = [0, 0, 0]
    for (i, battlefield_field) in enumerate(battlefield):
        if battlefield_field == player_id:
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

def max_on_board(player_id, players_houses, battlefield, roll):
    # deploy new player when possible
    our_positions = [-1]
    return_arr = [0, 0, 0]
    for (i, battlefield_field) in enumerate(battlefield):
        if battlefield_field == player_id:
            our_positions.append(i)

    if roll == 6:
        if 0 not in our_positions:
            if players_houses[player_id] > 0:
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

def aggressive(player_id, players_houses, battlefield, roll):
    # deploy new player when possible
    # kill when possible
    our_positions = []
    return_arr = [0, 0, 0]
    for (i, battlefield_field) in enumerate(battlefield):
        if battlefield_field == player_id:
            our_positions.append(i)

    for (i, our_position) in enumerate(our_positions):
        if our_position + roll <= 40:
            if battlefield[our_position + roll] != player_id:
                if battlefield[our_position + roll] != "-":
                    return_arr = [1, our_position, our_position + roll]
                    return return_arr
    if roll == 6:
        if 0 not in our_positions:
            if players_houses[player_id] > 0:
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

def smart_ai(player_id, players_houses, battlefield, roll):
    # deploy new player when we have less than 2 on battlefield and second player is in the second half
    # try to stay behind enemy players in first three quarters of the battlefield
    # kill when possible
    our_positions = []
    return_arr = [0, 0, 0]
    for (i, battlefield_field) in enumerate(battlefield):
        if battlefield_field == player_id:
            our_positions.append(i)

    for (i, our_position) in enumerate(our_positions):
        if our_position + roll <= 40:
            if battlefield[our_position + roll] != player_id:
                if battlefield[our_position + roll] != "-":
                    return_arr = [1, our_position, our_position + roll]
                    return return_arr
    if roll == 6:
        if 0 not in our_positions:
            if players_houses[player_id] > 0:
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

def init_battlefield():
    # Create 1D array to store players positions
    battlefield = [] #40
    i = 0
    while i <= 40:
        battlefield.append("-")
        i += 1
    return battlefield

def init_player_houses(players_num):
    i = 0
    players_houses = []
    while i <= players_num:
        players_houses.append(4)
        i += 1
    return players_houses

def init_player_finish(players_num):
    i = 0
    players_finish = []
    while i <= players_num:
        players_finish.append([0,0,0,0,1,1])
        i += 1
    return players_finish

def roll():
    # Random between 1-6
    return random.randint(1, 6)

def turn(player_id, players_houses, players_finish, battlefield, roll):
    """
    array request[int action(-1 = nothing, 0 = deploy, 1 = turn), int initial position, int new position]
    """
    request = [""]

    if player_id == 0:
        request = finish_one_by_one(player_id, players_houses, battlefield, roll)
    if player_id == 1:
        request = max_on_board(player_id, players_houses, battlefield, roll)
    if player_id == 2:
        request = aggressive(player_id, players_houses, battlefield, roll)
    if player_id == 3:
        request = smart_ai(player_id, players_houses, battlefield, roll)
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
        if not request[2] > 40:
            print("New position: " + str(request[2]))
        elif players_finish[player_id][(request[2] - 41)] != 0:
            print("Tried to finish but not possible, doing nothing")
        else:
            print("Finish" + "; Remaining in house: " + str(players_houses[player_id]))

    # Do what AI wants
    if request[0] == 0:
        players_houses[player_id] -= 1
        battlefield[0] = player_id
    elif request[0] == 1:
        if request[2] > 40:
            if players_finish[player_id][(request[2] - 41)] == 0:
                battlefield[request[1]] = "-"
        if not request[2] > 40:
            battlefield[request[1]] = "-"
            if battlefield[request[2]] != "-":
                players_houses[battlefield[request[2]]] += 1
            battlefield[request[2]] = player_id
        return 0

def game_status_refresh(player_id, players_houses, battlefield):
    # Check if there is winner
    # 0 = game is over, we have a winner!
    # 1 = game is running

    for (i, battlefield_field) in enumerate(battlefield):
        if battlefield_field == player_id:
            return 1
    if players_houses[player_id] == 0:
        return 0

print("pr01.py starting...")

players_num = 4

chart_run = 0
player_id = 0
game_status = 1

if len(sys.argv) > 1:
    # PyChart run requested, using sys.argv[1] as run count
    chart_run = 1
    run_counter = int(sys.argv[1]) - 1
    player_victories = [0, 0, 0, 0] # UGLY CODE!!! > Init manually for appropriate players count

print("Init battlefield...")
battlefield = init_battlefield()
players_finish = init_player_finish(players_num)

print("Init players...")
players_houses = init_player_houses(players_num)

while game_status != 0:
    while player_id <= players_num:
        roll_num = roll()
        turn(player_id, players_houses, players_finish, battlefield, roll_num)
        while roll_num == 6:
            roll_num = roll()
            turn(player_id, players_houses, players_finish, battlefield, roll_num)
        for (i, battlefield_field) in enumerate(battlefield):
            print(battlefield_field, end="")
        print("")
        game_status = game_status_refresh(player_id, players_houses, battlefield)
        if game_status == 0:
            print("Player " + str(player_id) + " won")
            if run_counter != 0 and chart_run == 1:
                # End of actual pass, reinit variables and run again
                game_status = 1
                print("Reinit battlefield...")
                battlefield = init_battlefield()
                players_finish = init_player_finish(players_num)
                print("Reinit players...")
                players_houses = init_player_houses(players_num)
                run_counter -= 1
                print("Run Counter: " + str(run_counter))
                player_victories[player_id] += 1
                print("Victories - " + str(player_victories))
                break
            break
        player_id += 1
        if player_id == players_num:
            player_id = 0

# Generate graph
if len(sys.argv) > 1:
    data = [go.Bar(
            x=['finish_one_by_one', 'max_on_board', 'aggressive', 'smart_ai'],
            y=player_victories
    )]

plotly.offline.plot(data, filename='basic-bar')