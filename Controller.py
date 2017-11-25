'''
Next step:
The optimization method where next moves were to be calculated in the draw function did not provide the
performance improvements expected. Game lags when larger window, e.g. 1000x1000, is used and computer is set to low
performance. Another approach will have to be utilized if a larger grid is to be used.
Variable window size depending on target machine.
'''

started = False
gameover = False
paused = True
configured = False #While started is false, this var checks if player has activated any cells. It will only become true when there is at least one cell active and will become false again if number of active cells decreases to zero while started is still false.
speed = 1
steps = 0
timeAtLastIteration = 0
origDelay = 200
delay = origDelay #in milliseconds
calculateNext = False
cellsToDie = set() #cells that will die.
cellsToLive = set()#cells that will live.

def restart(gameTimerMS, livingCells, grid, buttons):
    global started, paused, configured, steps, timeAtLastIteration
    started = False
    paused = True
    configured = False
    steps = 0
    timeAtLastIteration = 0

    #gameTimerMS = 0 #Doesnt work because floats are immutable. Whatever the hell that means...

    for livingCell in livingCells:
        grid[livingCell[0]][livingCell[1]] = 0
    livingCells = set()
    for button in buttons:
        button.setActiveImage(button.initialImage)

    return 0

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
    global speed, delay
    if speed == 1:
        speed = 2
        delay = origDelay - 100
        stepButton.setActiveImage("speed2")
        #print("speed 2 active")
    elif speed == 2:
        speed = 3
        delay = origDelay - 200
        stepButton.setActiveImage("speed3")
        #print("speed 3 active")
    elif speed == 3:
        speed = 1
        delay = origDelay
        stepButton.setActiveImage("speed1")
        #print("speed 1 active")
    #print(delay)

def step(livingCells, grid, blocksInRow, blocksInCol, timeAtLastIteration):
    global calculateNext
    if configured:
        if paused:
            #calculateNextMove(livingCells, grid, blocksInRow, blocksInCol, timeAtLastIteration)
            calculateNext = True
def cellClick(grid, row, column, livingCells):
    global configured
    if paused:
        if grid[row][column] == 1: #if cell is alive, kill
            grid[row][column] = 0
            livingCells.remove((row, column))
        elif grid[row][column] == 0: #if cell is dead, bring to life
            grid[row][column] = 1
            livingCells.add((row, column))
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

def calculateNextMove(livingCells, grid, blocksInRow, blocksInCol, timeAtLastIteration):

    globals()['timeAtLastIteration'] = timeAtLastIteration #differentiation between parameter and global variable with same name.
    cellsToDie = set() #cells that will die.
    cellsToLive = set()
    for row in range(blocksInRow):
        for column in range(blocksInCol):
            #deadNeighbours = 0
            livingNeighbours = 0
            #cell dies of isolation if at time t it has 0 or 1 neighbours
            #cell dies of overcrowding if at time t it has 4 or more neighbours
            #cell is born if at time t it is dead and has 3 live neighbours
            #check neighbours
            if row > 1 and column > 1: #upper left corner
                if grid[row - 1][column - 1] == 1:
                    livingNeighbours += 1
            if row > 1:                #above
                if grid[row - 1][column] == 1:
                    livingNeighbours += 1
            if row > 1 and column < blocksInRow - 1: #upper right corner
                if grid[row - 1][column + 1] == 1:
                    livingNeighbours += 1
            if column > 1: #left
                if grid[row][column - 1] == 1:
                    livingNeighbours += 1
            if column < blocksInRow - 1: #right
                if grid[row][column + 1] == 1:
                    livingNeighbours += 1
            if row < blocksInCol - 1 and column > 1: #bottom left corner
                if grid[row + 1][column - 1] == 1:
                    livingNeighbours += 1
            if row < blocksInCol - 1:           #underneath
                if grid[row + 1][column] == 1:
                    livingNeighbours += 1
            if row < blocksInCol - 1 and column < blocksInRow - 1: #bottom right corner
                if grid[row + 1][column + 1] == 1:
                    livingNeighbours += 1

            if grid[row][column] == 1:
                if livingNeighbours >= 4:
                    #cell will die of overcrowding
                    cellsToDie.add((row, column))
                elif livingNeighbours <= 1:
                    #cell will die of isolation
                    cellsToDie.add(((row, column)))
            elif grid[row][column] == 0:
                if livingNeighbours == 3:
                    #cell will be born
                    cellsToLive.add(((row, column)))
    for cellToLive in cellsToLive:
        livingCells.add(cellToLive)
        grid[cellToLive[0]][cellToLive[1]] = 1
    for cellToDie in cellsToDie:
        livingCells.remove(cellToDie)
        grid[cellToDie[0]][cellToDie[1]] = 0

def calculateNextCellMove(livingCells, grid, blocksInRow, blocksInCol, row, column):

    livingNeighbours = 0
    #cell dies of isolation if at time t it has 0 or 1 neighbours
    #cell dies of overcrowding if at time t it has 4 or more neighbours
    #cell is born if at time t it is dead and has 3 live neighbours
    #check neighbours
    if row > 1 and column > 1: #upper left corner
        if grid[row - 1][column - 1] == 1:
            livingNeighbours += 1
    if row > 1:                #above
        if grid[row - 1][column] == 1:
            livingNeighbours += 1
    if row > 1 and column < blocksInRow - 1: #upper right corner
        if grid[row - 1][column + 1] == 1:
            livingNeighbours += 1
    if column > 1: #left
        if grid[row][column - 1] == 1:
            livingNeighbours += 1
    if column < blocksInRow - 1: #right
        if grid[row][column + 1] == 1:
            livingNeighbours += 1
    if row < blocksInCol - 1 and column > 1: #bottom left corner
        if grid[row + 1][column - 1] == 1:
            livingNeighbours += 1
    if row < blocksInCol - 1:           #underneath
        if grid[row + 1][column] == 1:
            livingNeighbours += 1
    if row < blocksInCol - 1 and column < blocksInRow - 1: #bottom right corner
        if grid[row + 1][column + 1] == 1:
            livingNeighbours += 1

    if grid[row][column] == 1:
        if livingNeighbours >= 4:
            #cell will die of overcrowding
            cellsToDie.add((row, column))
        elif livingNeighbours <= 1:
            #cell will die of isolation
            cellsToDie.add(((row, column)))
    elif grid[row][column] == 0:
        if livingNeighbours == 3:
            #cell will be born
            cellsToLive.add(((row, column)))

def calculateNextMoveFinal(livingCells, grid, blocksInRow, blocksInCol, timeAtLastIteration):
    global cellsToLive, cellsToDie, calculateNext
    globals()['timeAtLastIteration'] = timeAtLastIteration #differentiation between parameter and global variable with same name.

    for cellToLive in cellsToLive:
        livingCells.add(cellToLive)
        grid[cellToLive[0]][cellToLive[1]] = 1
    for cellToDie in cellsToDie:
        livingCells.remove(cellToDie)
        grid[cellToDie[0]][cellToDie[1]] = 0
    cellsToLive = set()
    cellsToDie = set()
    calculateNext = False #added explicitly to disable next move calculation when step was used to calculate previous move

