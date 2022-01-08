# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 17:56:27 2021

@author: Bengee

@description:
    To calcualte the probability of drawing a 'good' hand from a draft deck,
    and then to see the change in probability when implimenting 'conspriacy'
    modifiers.

    This is done through a brute force simulation
"""

import numpy as np
import pandas as pd
import random as rn
import matplotlib.pyplot as plt

#==============================================================================
def simulation(deckSize, handSize, landMin, landMax, landInDeck, AP, BP):
    """
    Parameters
    ----------
    deckSize : int
        Number of cards in deck.
    handSize : int
        Number of cards in hand.
    landNeeded : int
        Number of lands needed for.
    landInDeck: int
        Number of lands in starting deck.
    AP : bool
        Advantaous Proclamation in play.
    BP : bool
        Backup Plan in play.

    Returns
    -------
    bool
        Hand is keepable or not.

    """
    # AP reduces decksize by 5, we assume landcount stays the same
    if AP:
        deckSize -= 5

    # Define a deck as being deckSize big, with landInDeck number of lands
    deck = [True if i < landInDeck else False for i in range(0,deckSize)]
    # Shuffle the deck
    deck = rn.sample(deck, len(deck))
    # Draw 7 cards, add 1 to land count everytime we draw a land
    firstHand = deck[0:handSize]

    # If we have BP draw second hand
    secondHand = []
    if BP:
        secondHand = deck[handSize:handSize + handSize]
    # If we drew a hand with ample lands return True, else False
    if sum(firstHand) in range(landMin, landMax + 1) \
    or sum(secondHand) in range(landMin, landMax + 1):
        return True
    else:
        return False
#==============================================================================

#==============================================================================
def makePlot(x, y, xlab, ylab):
    """
    Overview: Make a plot of x vs y
    """
    plt.plot(x,y)
    plt.title(ylab + " vs " + xlab)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xlim(x[0],x[len(x) -1])
    plt.ylim(0,100)
#==============================================================================

x = list(range(0, 40))
y = []
yAP = []
yBP = []
yAPBP = []
for land in x:
    trials = []
    trialsAP = []
    trialsBP = []
    trialsAPBP = []

    deckSize = 40
    handSize = 7
    landMin = 2
    landMax = 4
    landInDeck = land
    # AP = False
    # BP = True

    for i in range(0,10000):
         trials.append(simulation(deckSize, handSize, landMin, landMax, landInDeck, False, False))
         trialsAP.append(simulation(deckSize, handSize, landMin, landMax, landInDeck, True, False))
         trialsBP.append(simulation(deckSize, handSize, landMin, landMax, landInDeck, False, True))
         trialsAPBP.append(simulation(deckSize, handSize, landMin, landMax, landInDeck, True, True))

    result = 100 * sum(trials) / len(trials)
    resultAP = 100 * sum(trialsAP) / len(trialsAP)
    resultBP = 100 * sum(trialsBP) / len(trialsBP)
    resultAPBP = 100 * sum(trialsAPBP) / len(trialsAPBP)
    y.append(result)
    yAP.append(resultAP)
    yBP.append(resultBP)
    yAPBP.append(resultAPBP)
    # print("Deck Size: " + str(deckSize)  + "\n" +  "Hand Size: " + str(handSize) + "\n" \
    #     + "Minimum Lands: " + str(landMin)  + "\n"+ "Maximum Lands: " + str(landMax) + "\n" \
    #     + "Lands in Deck: " + str(landInDeck) + "\n"\
    #     + "Advantageous Proclemation: " + str(AP) + "\n" + "Backup Plan: " + str(BP) + "\n" \
    #     + "Odds of a good hand " + str(result) + "%")
makePlot(x,y,"Number of Lands in Deck", "Probability of a Good Hand (%)")
makePlot(x,yAP,"Number of Lands in Deck", "Probability of a Good Hand (%)")
makePlot(x,yBP,"Number of Lands in Deck", "Probability of a Good Hand (%)")
makePlot(x,yAPBP,"Number of Lands in Deck", "Probability of a Good Hand (%)")
plt.legend(["Default", "AP","BP","AP and BP"], loc ="best")
plt.grid()
plt.show()
