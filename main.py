#! /usr/bin/env python3

from functions import User, grid, multiRounds, clear
from time import sleep

playerOne = User()
playerTwo = User()
players = [playerOne, playerTwo]
gameboard = grid()

if playerOne.side == playerTwo.side:
	playerTwo.newSide()
	
print("-----------")
print("TIC TAC TOE")
print("-----------")
print("\nPress enter to continue")
input(">")
clear()

print("--------")
print("COMMANDS")
print("--------")
print("\n")
print("- Enter the corresponding co-ordinate where you want to play.")
print("- For example, 'a1' for the topmost square.")
print("- 'giveup' to give up for the round.")
print("\nPress enter to continue")
input(">")
clear()

print("-------------")
print("NAMING SCHEME")
print("-------------")
print("\n")
print("Enter player 1's name:")
playerOne.name = input(">")
print("\n")
print("Enter player 2's name:")
playerTwo.name = input(">")
sleep(1)
clear()

print("------------------")
print("CHOOSING X/O's....")
print("------------------")
sleep(1)
print("\n")
print(f"{playerOne.name}: {playerOne.letter}\n{playerTwo.name}: {playerTwo.letter}\n")
print("Press enter to continue")
input(">")
clear()

multiRounds(playerOne, playerTwo, gameboard)
