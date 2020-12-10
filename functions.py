#! /usr/bin/env python3

import random
from string import ascii_lowercase
from pandas import DataFrame
from os import system
from time import sleep
import platform

# Definitions

systemType = platform.system()

def clear():
    if systemType == "Windows":
        system("cls")
    elif systemType == "Linux" or systemType == "Darwin":
        system("clear")


# Classes


## Main User class to store name and side
class User():
    def __init__(self):
        self.name = None
        self.score = 0
        self.side = ChooseSide()
        if self.side == 0:
            self.letter = 'O'
        else:
            self.letter = 'X'

    def newSide(self):
        self.side = ChooseSide(chosen=True, prevside=self.side)
        if self.side == 0:
            self.letter = 'O'
        else:
            self.letter = 'X'


## Small class for co-ordinates
class CoOrds():
    def __init__(self, xcoord, ycoord: int):
        self.x = xcoord
        self.y = ycoord

    def __repr__(self):
        return f"{self.x}{self.y}"


## Main game space to play on
class grid():
    def __init__(self):
        self.a = ["-", "-", "-"]
        self.b = ["-", "-", "-"]
        self.c = ["-", "-", "-"]
        self.gridDict = {'a': self.a, 'b': self.b, 'c': self.c}

    def __repr__(self):
        total = DataFrame(
            self.gridDict,
            columns=['a', 'b', 'c'],
            index=[1, 2, 3],
            dtype="string").__repr__()
        return total

    def getItem(self, coords: CoOrds):
        if coords.x == 'a':
            changelist = self.a
        if coords.x == 'b':
            changelist = self.b
        if coords.x == 'c':
            changelist = self.c
        item = changelist[coords.y - 1]
        return item

    def play(self, side, coords: CoOrds):
        if coords.x == 'a':
            changelist = self.a
        if coords.x == 'b':
            changelist = self.b
        if coords.x == 'c':
            changelist = self.c

        if side == 1:
            letter = 'X'
        elif side == 0:
            letter = 'O'
        if changelist[coords.y - 1] == '-':
            changelist[coords.y - 1] = letter
    def totalList(self):
      x = self.a + self.b + self.c
      return x
# Functions


## Chooses side of user
def ChooseSide(chosen=False, prevside=None):
    if chosen == False:
        x = random.randrange(0, 2)
        return x
    else:
        if prevside == 1:
            return 0
        if prevside == 0:
            return 1


## Gets co-ordinates from user input
def getCoords(coordStr):
    if coordStr.strip() == "":
        return None
    coordList = [x for x in coordStr]
    try:
        coordList[1] = int(coordList[1])
        if not -1 < ascii_lowercase.index(coordList[0]) < 3:
            raise Exception
        return CoOrds(coordList[0], coordList[1])
    except:
        return None


## Checks for a win
def winCheck(player: User, self: grid):
    conditions = [
        self.a[0] == player.letter and self.a[1] == player.letter
        and self.a[2] == player.letter, self.b[0] == player.letter
        and self.b[1] == player.letter and self.b[2] == player.letter,
        self.c[0] == player.letter and self.c[1] == player.letter
        and self.c[2] == player.letter, self.a[0] == player.letter
        and self.b[1] == player.letter and self.c[2] == player.letter,
        self.c[0] == player.letter and self.b[1] == player.letter
        and self.a[2] == player.letter, self.a[0] == player.letter
        and self.b[0] == player.letter and self.c[0] == player.letter,
        self.a[1] == player.letter and self.b[1] == player.letter
        and self.c[1] == player.letter, self.a[2] == player.letter
        and self.b[2] == player.letter and self.c[2] == player.letter
    ]
    for condition in conditions:
        if condition:
            return True
            break


## Checks for a tie
def tieCheck(self: grid):
    if '-' in self.totalList():
      return
    else:
      return True
      
      
      


## Integrates both checks
def statCheck(player: User, gameboard: grid):
    wChecker = winCheck(player, gameboard)
    tChecker = tieCheck(gameboard)
    if wChecker is True:
        return 1
    if tChecker is True:
        return 2
    else:
        return 0


## Handles play from the input of coordinates
def inPlay(player: User, gameboard: grid, string: str):
    string = string.strip()
    if string == "giveup":
        return "giveup"
    coords = getCoords(string)
    if coords != None:
        if gameboard.getItem(coords) == "-":
            gameboard.play(player.side, coords)
            stats = statCheck(player, gameboard)
            return stats
    else:
        return None


## Individual Play
def onePlay(player: User, gameboard: grid):
    while True:
        clear()
        print("--------")
        print("GAMEPLAY")
        print("--------")
        print(f"It's {player.name}'s turn!")
        print("-------------")
        print(gameboard)
        print("-------------")
        print("Enter your coordinate to play eg. a1")
        incoord = input(">")
        stats = inPlay(player, gameboard, incoord)
        if stats != None:
            return stats
            break


## Handles Ties and Wins
def preStatHandler(player: User, stat):
    if stat == 1:
        player.score += 1
        return f"YAAY! {player.name} Won!"
    if stat == 2:
        return "It's a tie. So close and yet so far."
    if stat == 0:
        return None


def statHandler(player: User, gameboard: grid, stat):
    pStats = preStatHandler(player, stat)
    if pStats != None:
        system("clear")
        return f"{pStats}\n{gameboard}\n"
    else:
        return None


## Score Board
def scoreBoard(firstPlayer: User, secondPlayer: User):
    score = [firstPlayer.score, secondPlayer.score]
    x = DataFrame(
        score,
        index=[f"{firstPlayer.name}", f"{secondPlayer.name}"],
        columns=["Score"])
    return x.__repr__()


## Single Round
def singleRound(firstPlayer: User, secondPlayer: User, gameboard: grid):
    while True:
        pStat = onePlay(firstPlayer, gameboard)
        if pStat != "giveup":
            stats = statHandler(firstPlayer, gameboard, pStat)
            if stats != None:
                print(stats)
                break
        else:
            clear()
            print("You gave up :(")
            secondPlayer.score += 1
            print(gameboard)
            print("\n")
            break

        pStat = onePlay(secondPlayer, gameboard)
        if pStat != "giveup":
            stats = statHandler(secondPlayer, gameboard, pStat)
            if stats != None:
                print(stats)
                break
        else:
            clear()
            print("You gave up :(")
            firstPlayer.score += 1
            print(gameboard)
            print("\n")
            break
    sleep(3)
    clear()

    print("-----------")
    print("SCORE BOARD")
    print("-----------")
    score = scoreBoard(firstPlayer, secondPlayer)
    print(score)
    print("-----------")
    print("Press enter to play another round")
    input(">")


## Multiple Rounds
def multiRounds(firstPlayer: User, secondPlayer: User, gameboard: grid):
    while True:
        if firstPlayer.letter == 'X':
            startPlayer = firstPlayer
            auxPlayer = secondPlayer
        else:
            startPlayer = secondPlayer
            auxPlayer = firstPlayer
        singleRound(startPlayer, auxPlayer, gameboard)
        startPlayer.newSide()
        auxPlayer.newSide()
        del gameboard
        gameboard = grid()

