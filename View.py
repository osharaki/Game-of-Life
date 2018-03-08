'''
Next step:
Add text box to take configuration file path.
Variable window size depending on target machine.
Add functionality that counts cells, to better estimate distances when creating structures.
One suggestion would be "block shadows" that follow the cursor.
'''
import os

import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import Controller as controller

pygame.init()
pygame.font.init()

gameTimerMS = 0 #Time passed in milliseconds
gameTimerhms = (0, 0 , 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

windowHeight = 800
windowWidth = 1200

WIDTH = 5 # square width
HEIGHT = 5 # square height
MARGIN = 1  # distance between squares
oldWidth = WIDTH
oldHeight = HEIGHT
oldMargin = MARGIN
origWidth = WIDTH
origHeight = HEIGHT
origMargin = MARGIN
ommitedLines = 5 #Number of leading rows and columns that will not be rendered.

# Adjusts the screen size to make all grid blocks fit perfectly taking in regard margin size
while windowHeight % (HEIGHT + MARGIN) != 0:
    windowHeight += 1
blocksInCol = windowHeight//(HEIGHT + MARGIN)
while windowWidth % (WIDTH + MARGIN) != 0:
    windowWidth += 1
blocksInRow = windowWidth//(WIDTH + MARGIN)

blocksInRow += ommitedLines * 2
blocksInCol += ommitedLines * 2

maxZoomIn = 30
maxZoomOut = 2

#print(blocksInCol, ", ", blocksInRow)

dragVect = (0, 0)



surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Game of Life')

#Mouse Variables
lastMousePos = pygame.mouse.get_pos()
mouseStates = None
mouseDown = False


# screen text
fontPath = os.path.join("assets", "fonts", "LemonMilk.otf") #makes path platform independent
font = pygame.font.Font(fontPath, 40)

grid = [[0 for x in range(blocksInRow)] for y in range(blocksInCol)]
#gridPos = [[[(MARGIN + WIDTH) * x + MARGIN, (MARGIN + HEIGHT) * y + MARGIN] for x in range(blocksInRow)] for y in range(blocksInCol)]
gridPos = [[[(MARGIN + WIDTH) * (x + ommitedLines * -1) + MARGIN, (MARGIN + HEIGHT) * (y + ommitedLines * -1) + MARGIN] for x in range(blocksInRow)] for y in range(blocksInCol)]
livingCells = set() #Saves the coordinates (row, col) of live cells.
#print(grid)

#print(gridPos)
#print(gridPos)

class Button():
    def __init__(self, name, order, state, imagePaths, initialImage):
        self.state = state #controls whether the image is to be drawn or not
        self.name = name #button alias
        self.order = order #where on the screen the button is to appear. 1 is rightmost image
        self.imageDict = {} #maps image alias to image object to ease later referencing
        self.initialImage = initialImage

        for imageName in imagePaths:
            self.imageDict[imageName] = pygame.image.load(imagePaths[imageName])

        self.image = self.imageDict[initialImage]
        self.imageSize = self.image.get_rect().size
        self.width = self.imageSize[0]
        self.height = self.imageSize[1]
        self.pos = (windowWidth - self.width, 0)

    def setActiveImage(self, imageName):
        self.image = self.imageDict[imageName]

'''
Draws buttons, bearing in mind their order attribute, meaning objects will be lined up side by side at the top of the
screen.
'''
def drawButtons(buttonList):
    i = 1
    for button in buttonList:
        if button.order == i:

            if i != 1:
                button.pos = (lastButton.pos[0] - button.width, button.pos[1])
            i += 1
            lastButton = button
            if button.state:
                surface.blit(button.image, button.pos)

pausePlayButton = Button("pausePlayButton", 1, True, {"pause" : os.path.join("assets", "images", "pause-button.png"), "play" : os.path.join("assets", "images", "play-button.png")}, "play")
stepButton = Button("stepButton", 2, True, {"step" : os.path.join("assets", "images", "step25x25.png"), "step_disabled" : os.path.join("assets", "images", "step25x25_disabled.png")}, "step_disabled")
speedButton = Button("speedButton", 3, True, {"speed1" : os.path.join("assets", "images", "speed1.png"), "speed2" : os.path.join("assets", "images", "speed2.png"), "speed3" : os.path.join("assets", "images", "speed3.png")}, "speed1")
restartButton = Button("restartButton", 4, True, {"restart" : os.path.join("assets", "images", "restart-button.png")}, "restart")
readButton = Button("readButton", 5, True, {"read" : os.path.join("assets", "images", "read.png")}, "read")
buttons = [pausePlayButton, stepButton, speedButton, restartButton, readButton]

'''
Checks if buttons have been clicked and calls the appropriate controller functions.
'''
def HandleClicks(clickPos):
    global gameTimerMS
    for button in buttons:
        if clickPos[0] >= button.pos[0] and clickPos[0] <= button.pos[0] + button.width\
            and clickPos[1] >= button.pos[1] and clickPos[1] <= button.pos[1] + button.height:
            if button.name == "pausePlayButton":
                controller.pausePlayHandler(buttons)
            elif button.name == "stepButton":
                controller.step(livingCells, grid, blocksInRow, blocksInCol, gameTimerMS)
            elif button.name == "speedButton":
                controller.speedAdjust(button)
            elif button.name == "restartButton":
                gameTimerMS = controller.restart(gameTimerMS, livingCells, grid, buttons)
                #print(livingCells)
            elif button.name == "readButton":
                controller.readConfig("C:/Users/Owner/PyCharmProjects/Game of Life/configs/glider-gun.txt", grid, livingCells, blocksInCol//2, blocksInRow//2)
            return #if a button has been pressed, no need to keep searching

    for row in range(blocksInCol):
        #look for correct row
        if clickPos[1] >= gridPos[row][0][1] and clickPos[1] <= gridPos[row][0][1] + HEIGHT:
            #found correct row, now look for column
            for column in range(blocksInRow):
                if clickPos[0] >= gridPos[row][column][0] and clickPos[0] <= gridPos[row][column][0] + WIDTH:
                    #found correct column
                    controller.cellClick(grid, row, column, livingCells)

'''
The only part of the grid that is drawn are living cells.
'''
def drawGrid():

    global dragVect

    surface.fill(WHITE)
    #oldDragVect = dragVect
    # Draw the live cells
    #print(livingCells)
    for livingCell in livingCells:
        color = BLACK

        if livingCell[0] > (ommitedLines - 1) and livingCell[0] < (blocksInCol - ommitedLines) and livingCell[1] > (ommitedLines - 1) and livingCell[1] < (blocksInRow - ommitedLines):
            pygame.draw.rect(surface,
                             color,
                             [gridPos[livingCell[0]][livingCell[1]][0],
                             gridPos[livingCell[0]][livingCell[1]][1],
                             WIDTH,
                             HEIGHT])

'''
Draws time progression.
'''
def drawTime():
    currentTime = controller.formatTimeString(gameTimerhms)
    ren = font.render(currentTime, 0, BLACK, WHITE)
    surface.blit(ren, (0, 0))

'''
Draws iterations.
'''
def drawIterations():
    ren = font.render("Gen.: " + str(controller.steps), 0, BLACK, WHITE)
    surface.blit(ren, (10, 0))

def quitGame():
    pygame.quit()
    sys.exit()

clock = pygame.time.Clock()

while True:
    if not controller.paused: #Time only progresses if game is not paused.
        gameTimerMS += clock.get_time()
        #print(controller.delay)
        if gameTimerMS - controller.timeAtLastIteration >= controller.delay:
            controller.calculateNextMove(livingCells, grid, blocksInRow, blocksInCol, gameTimerMS)
    gameTimerhms = controller.calculateTime(gameTimerMS)

    drawGrid()
    drawIterations()
    drawButtons(buttons)
    #drawButtons()
    # Handle user and system events
    for event in GAME_EVENTS.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clickPos = pygame.mouse.get_pos()
                HandleClicks(clickPos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    clock.tick(60)
    pygame.display.update()