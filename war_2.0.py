#!/usr/bin/env python3

#War 2.0 
#1.1 Fixed edge case where if you ran out of cars to 'War' with as your last card, it crashed.
#1.2 Fixed when a player has 3 cards left, the loop declares a winner before the results of the war.
#2.0 Added stat tracking that saves through iterations using pickle
#    Added better comments for various parts of the code.
#    Re-wrote parts of the code for better readability, and some code is more efficient.

#TODO:
#Add output to show what cards you win from the other player during a war

import random
import time
import sys
import pickle
from operator import itemgetter

#Variables to count if war, provide output,
#track single game stats, and lifetime stats.
playTotal = 0
warTotal = 0
doubleWarTotal = 0
tripleWarTotal = 0
worldWarTotal = 0
playerOneWins = 0
playerTwoWins = 0
gamesPlayed = 0
war = 0 

#Lists for building your deck of cards
faces = ['2', '3', '4', '5', '6', '7', '8',
         '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
deck = []       #your deck of cards
handP1 = []     #player one's hand
handP2 = []     #player two's hand
warHandP1 = []  #stores player one's cards during a war 
warHandP2 = []  #stores player two's cards during a war
'''
#might need a list or two more for the stats to save/load
'''
#Create a deck of cards from the lists faces and suits.
def buildDeck():
    
    for x in faces:
        for y in suits:
            card = x + ' of ' + y
            deck.append(card)

    random.shuffle(deck)
    dealCards()
    
def dealCards():
    
    x = len(deck)
    while x > 0:
        p1Card = random.choice(deck)
        handP1.append(p1Card)
        deck.remove(p1Card)
        p2Card = random.choice(deck)
        handP2.append(p2Card)
        deck.remove(p2Card)
        x -= 2
    print(len(handP1))
    print(len(handP2))
    checkForDuplicates()
 
#Function to check for duplicate cards in your hands.
#You can comment out the print statements if you don't want them.
def checkForDuplicates():
    
    for x, y in zip(handP1, handP2):
        if x == y:
            print('You have duplicate cards.')
        else:
            print('P1: ', x, 'P2: ', y)
    playWar(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
         worldWarTotal, war)

def playWar(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
         worldWarTotal, war):
    
    while len(handP1) != 0 or len(handP2) != 0:
        time.sleep(0)   #adjust how fast you see ouput
        print(war)
        if war == 0:
            print('\nPlay!\n')
            playTotal += 1
        if war == 1: 
            print('\n*War!*\n')
            warTotal += 1
        if war == 2: 
            print('\n**Double War!!**\n')
            doubleWarTotal += 1
        if war == 3:
            print('\n***Triple War!!!***\n')
            tripleWarTotal += 1
        if war >= 4:
            print('\n******~~~~~~!!! WORLD WAR !!!~~~~~~******\n')
            worldWarTotal += 1
        card1 = itemgetter(0)(handP1)   #Grabs the first item from handP1
        value1 = card1[0]               #Slices the string to get the cards value
        card2 = itemgetter(0)(handP2)   #Grabs the first item from handP2
        value2 = card2[0]               #Slices the string to get the cards value
        print('Player 1 shows: ', card1)
        print('Player 2 shows: ', card2)
               
        #Reassigning numbers to the lettered cards and,
        #10's were being stored as 1 from the string slice, so this fixes that too.            
        if value1 == '1':
            value1 = '10'
        if value2 == '1':
            value2 = '10'
        if value1 == 'J':
            value1 = '11'
        if value2 == 'J':
            value2 = '11'
        if value1 == 'Q':
            value1 = '12'
        if value2 == 'Q':
            value2 = '12'
        if value1 == 'K':
            value1 = '13'
        if value2 == 'K':
            value2 = '13'
        if value1 == 'A':
            value1 = '14'
        if value2 == 'A':
            value2 = '14'     
        
        #Compare the values of the cards in the next 3 if statements.
        if int(value1) > int(value2):
            handP1.append(card2)
            for x in warHandP1:
                handP1.append(x)
            for x in warHandP2:
                handP1.append(x)
            warHandP1.clear()
            warHandP2.clear()
            handP2.remove(card2)
            #Move your card to the bottom of your deck.
            handP1.append(handP1.pop(handP1.index(card1)))
            war = 0
            print('Cards remaining for Player 1: ', len(handP1))
            print('Cards remaining for Player 2: ', len(handP2))
         
        if int(value2) > int(value1):
            handP2.append(card1)
            for x in warHandP1:
                handP2.append(x)
            for x in warHandP2:
                handP2.append(x)
            warHandP1.clear()
            warHandP2.clear()
            handP1.remove(card1)
            #Move your card to the bottom of your deck.
            handP2.append(handP2.pop(handP2.index(card2)))
            war = 0
            print('Cards remaining for Player 1: ', len(handP1))
            print('Cards remaining for Player 2: ', len(handP2))         
            
        if int(value1) == int(value2):
            #This will start a war.
            #Increase how many loops the war is in for message output.
            war += 1
            warHandP1.append(card1)
            warHandP2.append(card2)
            handP1.remove(card1)
            handP2.remove(card2)
            winner(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
                       worldWarTotal, playerOneWins, playerTwoWins)            
            #Each player places 1 card 'facedown'.
            facedown1 = itemgetter(0)(handP1)
            warHandP1.append(facedown1)
            handP1.remove(facedown1)
            facedown2 = itemgetter(0)(handP2)
            warHandP2.append(facedown2)
            handP2.remove(facedown2)
        winner(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
               worldWarTotal, playerOneWins, playerTwoWins)     

#Test to see if we have a winner!        
def winner(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
         worldWarTotal, playerOneWins, playerTwoWins):
    if len(handP1) == 0:
        playerTwoWins += 1
        print('\nPlayer 2 Wins!!\n')
        print('^^^Game Stats^^^')
        print('Play Total: ', playTotal)
        print('War Total: ', warTotal)
        print('Double War Total: ', doubleWarTotal)
        print('Triple War Total: ', tripleWarTotal)
        print('World War Total: ', worldWarTotal)
        savedStats(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
               worldWarTotal, playerOneWins, playerTwoWins, gamesPlayed)
        sys.exit()
    elif len(handP2) == 0:
        playerOneWins += 1
        print('\nPlayer 1 Wins!!\n')
        print('^^^Game Stats^^^')
        print('Play Total: ', playTotal)
        print('War Total: ', warTotal)
        print('Double War Total: ', doubleWarTotal)
        print('Triple War Total: ', tripleWarTotal)
        print('World War Total: ', worldWarTotal)
        savedStats(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
               worldWarTotal, playerOneWins, playerTwoWins, gamesPlayed)
        sys.exit()

#Print stats from your game, print totals for lifetime stats, and saves game.
def savedStats(playTotal, warTotal, doubleWarTotal, tripleWarTotal,
               worldWarTotal, playerOneWins, playerTwoWins, gamesPlayed):
    gamesPlayed += 1
    gameStats = [playTotal, warTotal, doubleWarTotal, tripleWarTotal,
               worldWarTotal, playerOneWins, playerTwoWins, gamesPlayed]
    newTotal = []
    allStats = ['Play Total: ', 'War Total: ', 'Double War Total: ',
                'Triple War Total: ', 'World War Total: ', 
                'Player One Wins: ', 'Player 2 Wins: ', 'Games Played: ']
    try:
        saveFile = open('save.dat', 'rb')
        prevData = pickle.load(saveFile)
        for x, y in zip(prevData, gameStats):
            number = x + y
            newTotal.append(number)
        saveFile.close()
        saveFile = open('save.dat', 'wb')
        pickle.dump(newTotal, saveFile, protocol=pickle.HIGHEST_PROTOCOL)
        saveFile.close()
    except FileNotFoundError:
        saveFile = open('save.dat', 'wb')
        pickle.dump(gameStats, saveFile, protocol=pickle.HIGHEST_PROTOCOL)
        saveFile.close()
    print('\n-----Total Stats-----')
    for x, y in zip(allStats, newTotal):
        stats = str(x) + str(y)
        print(stats)
    print('----------------------')

if __name__ == '__main__':        
    buildDeck()

    
            
    
