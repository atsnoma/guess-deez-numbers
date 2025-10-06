import random
import math
import sys
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
def levelManagement(totScore, level, playerHealth, skipPassTokens, roundOffTokens, directionDetection):
    wincondition = victoryCheck(totScore)
    if wincondition == True:
        sys.exit
    else:
        level += 1
        playerHealth += 1+level
        print("You have %i health, as well as %i Skip Tokens and %i Rounding Tokens. Your Detection Level is at %i." % (playerHealth, skipPassTokens, roundOffTokens, directionDetection))
        level, skipPassTokens, roundOffTokens = checkupTokens(level, skipPassTokens, roundOffTokens)
        directionDetection = checkupUpgrades(level,directionDetection)
        input("Press Enter to Continue...")
        print("The highest possible number for this round is %i!" % (4*level + 1))
        startGame(level, playerHealth, totScore, skipPassTokens, roundOffTokens, directionDetection)

#This handles restocking of tokens
def checkupTokens(level, skipPassTokens, roundOffTokens):
    if level < 4:
        return level, skipPassTokens, roundOffTokens
    elif level == 4:
        print("You now have access to Round off and Skip Tokens!")
        print("Type \'Skip\' or \'Round\' to use them.")
        roundOffTokens = 3
        skipPassTokens = 3
        print("Added 3 Skip Tokens")
        print("Added 3 Round Tokens")
        return level, skipPassTokens, roundOffTokens
    else:
        while True:
                skipInput = input("Would you like any more Skip Tokens? The game will get harder if you do! (Y/N)")
                if skipInput.lower() == "y" :
                    skipPassTokens += math.floor(level/2)
                    level += 1
                    print("Added ", math.floor(level/2), " Skip Tokens.")
                    break
                elif skipInput.lower() == "n" :
                    break
                else:
                    print("Please type either \'Y\' or \'N\'.")
        while True:
            roundInput = input("Would you like any more Round Tokens? The game will get harder if you do! (Y/N)")
            if roundInput.lower() == "y" :
                roundOffTokens += math.floor(level/2)
                level += 1
                print("Added ", math.floor(level/2), " Round Tokens.")
                break
            
            elif roundInput.lower() == "n" :
                break
            else:
                print("Please type either \'Y\' or \'N\'.")
        return level, skipPassTokens, roundOffTokens

#This handles the upgrading of Math Sense
def checkupUpgrades(level, directionDetection):
    if level < 3:
        return directionDetection
    elif level == 3:
        directionDetection += 1
        print("You now have a better sense for numbers! Detection increased by 1.")
        return directionDetection
    else:
        while True:
            upgradeInput = input("Your Number Sense is currently level %i. Would you like to upgrade it? (Y/N)" % (directionDetection))
            if upgradeInput.lower() == "y" :
                directionDetection += 1
                print("Your Number Sense has increased.")
                break
            elif upgradeInput.lower() == "n" :
                break
            else:
                print("Please type either \'Y\' or \'N\'.")
    return directionDetection

#This starts the next round of the game.
def startGame(level, playerHealth, totScore, skipPassTokens, roundOffTokens, directionDetection):
    for i in range (level+1):
        playerHealth, totScore, skipPassTokens, roundOffTokens = nextNumber(level, playerHealth, totScore, skipPassTokens, roundOffTokens, directionDetection)
        if playerHealth == 0:
            break
    else:
        levelManagement(totScore, level, playerHealth, skipPassTokens, roundOffTokens, directionDetection)

#This function generates a random number for each battle. The initial starting values are 0 and 5.
def generateNumber(level):
    minimumNumber = 0
    maximumNumber = 1
    maximumNumber += 4*level
    return random.randrange(minimumNumber, maximumNumber)

#This function handles events during a correct guess.
def correctGuess(level, targetNumber, totScore):
    print("That is correct! The number was", targetNumber, "!")
    totScore += 1+level
    return totScore

#This function handles events during an incorrect guess.
def incorrectGuess(playerHealth, totScore, directionDetection, playerGuess, targetNumber):
    playerHealth -= 1
    if directionDetection > 0:
        learnNumber(playerGuess, targetNumber, directionDetection)
    if playerHealth == 0:
        gameOver(totScore)
        return playerHealth, totScore
    else:
        print("Wrong! Lives remaining: ", playerHealth)
        totScore -= 1
        return playerHealth, totScore

#This function handles hints after WRONG guesses
def learnNumber(playerGuess, targetNumber, directionDetection):
    if directionDetection > 0:
        try:
            if int(playerGuess) > targetNumber:
                print("The number is lesser than your guess!")
            else:
                print("The number is greater than your guess!")
        except:
            pass
    if directionDetection > 1:
            predictNumber = targetNumber - random.randrange(1, 10)
            print("The number is greater than %i!" % (predictNumber))
    if directionDetection > 2:
            predictNumber2 = targetNumber + random.randrange(1, 10)
            print("The number is lesser than %i!" % (predictNumber2))
    return
#This function handles hints before any guesses.
def hintNumber(targetNumber, directionDetection):
    if directionDetection > 0:
        factorNumber = None
        for i in range (2,9):
            divisibilityNumber = targetNumber % i
            if divisibilityNumber == 0:
                factorNumber = i
            else:
                pass
        if factorNumber != None:
            print("The number is divisible by ", factorNumber, "!")
        else:
            print("The number is not divisble by numbers 2 through 9!")
    if directionDetection > 2:
        lastNumber = targetNumber % 10
        print("The number ends in a %i!" % (lastNumber))
    return
        

#This function handles the use of Round Tokens
def useRoundToken(targetNumber):
    randomRounder = random.randrange(5, 10, 5)
    tempNumber = targetNumber % randomRounder
    targetNumber -= tempNumber
    print("The number is now divisible by", randomRounder, "rounded down!")
    return targetNumber

#This function handles each battle and directly implements Skip Tokens
def nextNumber(level, playerHealth, totScore, skipPassTokens, roundOffTokens, directionDetection):
    targetNumber = int(generateNumber(level))
    print(targetNumber)
    if directionDetection > 0:
        hintNumber(targetNumber, directionDetection)
    while playerHealth > 0:
            playerGuess = input("Take a Guess: ")
            if playerGuess.lower() == "skip":
                if skipPassTokens > 0:
                    skipPassTokens -= 1
                    totScore = correctGuess(level, targetNumber, totScore)
                    return playerHealth, totScore, skipPassTokens, roundOffTokens
                else:
                    print("No skip tokens remaining!")
                    continue
            if playerGuess.lower() == "round":
                if roundOffTokens > 0:
                    roundOffTokens -= 1
                    targetNumber = useRoundToken(targetNumber)
                    continue
                else:
                    print("No round tokens remaining!")
                    continue
            try:
                if int(playerGuess) == targetNumber:
                    totScore = correctGuess(level, targetNumber, totScore)
                    return playerHealth, totScore, skipPassTokens, roundOffTokens
                elif playerHealth == 0:
                    return playerHealth, totScore, skipPassTokens, roundOffTokens
                else:
                    (playerHealth, totScore) = incorrectGuess(playerHealth, totScore, directionDetection, playerGuess, targetNumber)
            except:
                (playerHealth, totScore) = incorrectGuess(playerHealth, totScore, directionDetection, playerGuess, targetNumber)

#This function handles a game over.
def gameOver(totScore):
    print("You are out of guesses. Everything is lost.")
    print("Total Score:", totScore)
    return

#This function handles victory.
def victoryCheck(totScore):
    if totScore > 150:
        print("You have defended the people! You are a true hero.")
        print("Final Score: %i" % (totScore))
        input("Press Enter to exit the game as a winner!")
        wincondition = True
        return wincondition
    else:
        wincondition = False
        return wincondition
    
#This starts the first round
print("The town of Marshall's Mound is under attack! Only you, a math wizard, can prevent complete calamity.")
print("Your spell-slinging is best represented by the challenge of guessing a number between 0 and 5, but it will get harder over time!")
startGame(level, playerHealth, totScore, skipPassTokens, roundOffTokens, directionDetection)
