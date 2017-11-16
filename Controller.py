'''
Next step: Speed adjustment functionality will be disabled.
The actual game of life function can now be developed and the other functions augmented to accommodate it.
The restart button still needs to be added.
'''



started = False
gameover = False
paused = True
configured = False #While started is false, this var checks if player has activated any cells. It will only become true when there is at least one cell active and will become false again if number of active cells decreases to zero while started is still false.
speed = 1
steps = 0

'''
Called when pause/play button is clicked.
'''
def pausePlayHandler(buttons):
    global paused
    global started
    if configured: #if player has activated some cells the game may be started
        if paused: #game will now be running
            started = True
            paused = False
            for button in buttons: #find step button
                if button.name == "stepButton":
                    button.image = button.imageDict["step_disabled"] #step must be disabled
                if button.name == "pausePlayButton":
                    button.image = button.imageDict["pause"] #change icon to pause
        else: #game will be paused
            paused = True
            for button in buttons: #find step button
                if button.name == "stepButton":
                    button.image = button.imageDict["step"] #step may be enabled
                if button.name == "pausePlayButton":
                    button.image = button.imageDict["play"] #change icon to play
    #print("pause/play clicked!")


def speedAdjust(stepButton):
    global speed
    if speed == 1:
        speed = 2
        stepButton.setActiveImage("speed2")
        #print("speed 2 active")
    elif speed == 2:
        speed = 3
        stepButton.setActiveImage("speed3")
        #print("speed 3 active")
    elif speed == 3:
        speed = 1
        stepButton.setActiveImage("speed1")
        #print("speed 1 active")


def step():
    if configured:
        if paused:
            nextMove()


def nextMove():
    print("the next move is being calculated")

def cellClick(grid, row, column, livingCells):
    global configured
    if paused:
        if grid[row][column] == 1: #if cell is alive, kill
            grid[row][column] = 0
            livingCells.remove([row, column])
        elif grid[row][column] == 0: #if cell is dead, bring to life
            grid[row][column] = 1
            livingCells.append([row, column])
        if not started: #If game hasn't been started yet, configured should be updated according to the cell states.
                        #This prevents a game from being started when all cells are dead.
            if len(livingCells) == 0:
                configured = False
            else:
                configured = True
        #print(livingCells)
        #print(configured)

'''
Turns milliseconds to hours:minutes:seconds.
'''
def calculateTime(milliseconds):
    seconds = int((milliseconds / 1000) % 60)
    minutes = int(((milliseconds / (1000*60)) % 60))
    hours = int(((milliseconds / (1000*60*60)) % 24))

    return (hours, minutes, seconds)

'''
Adds a leading zero to single digit time components.
'''
def formatTimeString(gameTimerhms):
    currentTime = ""
    if (gameTimerhms[0] // 10) != 0:
        currentTime += str(gameTimerhms[0]) + ":"
    else:
        currentTime += "0" + str(gameTimerhms[0]) + ":"
    if (gameTimerhms[1] // 10) != 0:
        currentTime += str(gameTimerhms[1]) + ":"
    else:
        currentTime += "0" + str(gameTimerhms[1]) + ":"
    if (gameTimerhms[2] // 10) != 0:
        currentTime += str(gameTimerhms[2])
    else:
        currentTime += "0" + str(gameTimerhms[2])

    return currentTime

def calculateNextMove():

    #cell dies of isolation if at time t it has 0 or 1 neighbours

    #cell dies of overcrowding if at time t it has 4 or more neighbours

    #cell is born if at time 