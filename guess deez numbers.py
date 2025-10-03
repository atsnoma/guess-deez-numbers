import random
import math
'''

This is a number guessing roguelike

'''
totScore = 0
playerHealth = 5
directionDetection = 0
roundOffTokens = 0
skipPassTokens = 0
level = 1

#This controls level changes and reports resources to the player between rounds.
def levelManagement(level, playerHealth, skipPassTokens, roundOffTokens, directionDetection):
    level += 1
    playerHealth += 1+level
    print("You have %i health, as well as %i Skip Tokens and %i Rounding Tokens. Your Detection Level is at %i." % (playerHealth, skipPassTokens, roundOffTokens, directionDetection))
    roundOffTokens, skipPassTokens = checkupTokens(level, roundOffTokens, skipPassTokens)
    checkupUpgrades(level)
    input("Press Any Key to Continue...")
    startGame(level, playerHealth, totScore)

#This handles restocking of tokens
def checkupTokens(level, roundOffTokens, skipPassTokens):
    if level < 4:
        return
    elif level == 4:
        print("You now have access to Round off and Skip Tokens!")
        roundOffTokens = 3
        skipPassTokens = 3
        print("Added 3 Skip Tokens")
        print("Added 3 Round Tokens")
    else:
        pass
    try:
        skipInput = input("Would you like any more Skip Tokens? The game will get harder if you do! (Y/N)")
        if skipInput == "Y" :
            skipPassTokens += math.floor(level/2)
            level += 1
            print("Added " + math.floor(level/2) + " Skip Tokens.")
            pass
        elif skipInput == "N" :
            pass
        else:
            print("Please type either \'Y\' or \'N\'.")
    except:
        print ("No tokens today.")
        pass
    try:
        roundInput = input("Would you like any more Round Tokens? The game will get harder if you do! (Y/N)")
        if roundInput == "Y" :
            roundOffTokens += math.floor(level/2)
            level += 1
            print("Added " + math.floor(level/2) + " Round Tokens.")
            return roundOffTokens, skipPassTokens
        elif roundInput == "N" :
            return roundOffTokens, skipPassTokens
        else:
            print("Please type either \'Y\' or \'N\'.")
    except:
        print ("No tokens today.")
        return roundOffTokens, skipPassTokens

def checkupUpgrades():
    if level < 5:
        return
    elif level == 5:
        "You now have a better sense numbers!"
    else:
        pass
    try:
        upgradeInput = ("Your Number Sense is currently level " + directionDetection + ". Would you like to upgrade it? (Y/N)")
        if upgradeInput == "Y" :
            directionDetection += 1
            print("Your number sense has increased.")
            return
        elif upgradeInput == "N" :
            return
        else:
            print("Please type either \'Y\' or \'N\'.")
    except:
        print ("No tokens today.")
        return

#This starts the next round of the game.
def startGame(level, playerHealth, totScore):
    for i in range (level+1):
        playerHealth, totScore = nextNumber(level, playerHealth, totScore, directionDetection)
        if playerHealth == 0:
            break
    else:
        levelManagement(level, playerHealth, skipPassTokens, roundOffTokens, directionDetection)

#This function generates a random number for each battle.
def generateNumber(level):
    minimumNumber = 0
    maximumNumber = 10
    minimumNumber -= 2*level
    maximumNumber += 2*level
    return random.randrange(minimumNumber, maximumNumber)

#This function handles events during a correct guess.
def correctGuess(targetNumber, totScore):
    print("That is correct! The number was", targetNumber, "!")
    totScore += 1+level
    return totScore

#This function handles events during an incorrect guess.
def incorrectGuess(playerHealth, totScore):
    playerHealth -= 1
    if playerHealth == 0:
        gameOver(totScore)
        return playerHealth, totScore
    else:
        print("Wrong! Lives remaining: ", playerHealth)
        totScore -= 1
        return playerHealth, totScore
    if directionDetection > 1:
        learningNumber()

#This function handles direction detection hints on incorrect guesses.
#def learningNumber():
#    if targetNumber

#This function handles hints before any guesses.
def hintNumber():
    if targetNumber > 0 :
        print("The number is positive!")
    else :
        print ("The number is negative!")
    if directionDetection > 2:
        for i in range (2,9):
            divisibilityNumber = targetNumber % i
            if divisibilityNumber == 0:
                factorNumber = i
            else:
                pass
        if factorNumber != None:
            print("The number is divisible by " + factorNumber + "!")
        else:
            print("The number is not divisble by numbers 2 through 9!")
    
#This function handles each battle.
def nextNumber(level, playerHealth, totScore, directionDetection):
    targetNumber = int(generateNumber(level))
    print(targetNumber)
    if directionDetection > 0:
        hintNumber()
    while playerHealth > 0:
        playerGuess = int(input("Take a Guess: "))
        if playerGuess == targetNumber:
            totScore = correctGuess(targetNumber, totScore)
            return playerHealth, totScore
        (playerHealth, totScore) = incorrectGuess(playerHealth, totScore)
        if playerHealth == 0:
            return playerHealth, totScore
#This function handles the end of the game.
def gameOver(totScore):
    print("You are out of guesses. Everything is lost.")
    print("Total Score:", totScore)
    return



#This starts the first round
print("Welcome to Guess Deez Numbers!")
print("Your job is to guess a number between 0 and 10, but it will get harder over time!")
startGame(level, playerHealth, totScore)
