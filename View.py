'''
Next step: Speed adjustment functionality will be disabled.
Variable window size depending on target machine.
The restart button still needs to be added.
'''
#This is a test line to test the second commit on the new branch
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

windowHeight = 500
windowWidth = 500

WIDTH = 10 # square width
HEIGHT = 10 # square height
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
font = pygame.font.Font(None, 40)

'''
ren1 = font.render("Test", 0, RED)
ren2 = font.render("Test", 0, RED)
ren3 = font.render("Test", 0, RED)
ren4 = font.render("Test", 0, RED)
ren5 = font.render("Test", 0, RED)
ren6 = font.render("Test", 0, RED)
'''

grid = [[0 for x in range(blocksInRow)] for y in range(blocksInCol)]
#gridPos = [[[(MARGIN + WIDTH) * x + MARGIN, (MARGIN + HEIGHT) * y + MARGIN] for x in range(blocksInRow)] for y in range(blocksInCol)]
gridPos = [[[(MARGIN + WIDTH) * (x + ommitedLines * -1) + MARGIN, (MARGIN + HEIGHT) * (y + ommitedLines * -1) + MARGIN] for x in range(blocksInRow)] for y in range(blocksInCol)]
livingCells = set() #Saves the coordinates (row, col) of live cells.
#print(gridPos)

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

pausePlayButton = Button("pausePlayButton", 1, True, {"pause" : "assets/images/pause-button.png", "play" : "assets/images/play-button.png"}, "play")
stepButton = Button("stepButton", 2, True, {"step" : "assets/images/step25x25.png", "step_disabled" : "assets/images/step25x25_disabled.png"}, "step_disabled")
speedButton = Button("speedButton", 3, True, {"speed1" : "assets/images/speed1.png", "speed2" : "assets/images/speed2.png", "speed3" : "assets/images/speed3.png"}, "speed1")
restartButton = Button("restartButton", 4, True, {"restart" : "assets/images/restart-button.png"}, "restart")
buttons = [pausePlayButton, stepButton, speedButton, restartButton]

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
            return #if a button has been pressed, no need to keep searching
    '''
    for row in range(blocksInRow):
        for column in range(blocksInCol):
            if clickPos[0] >= gridPos[row][column][0] and clickPos[0] <= gridPos[row][column][0] + WIDTH\
                and clickPos[1] >= gridPos[row][column][1] and clickPos[1] <= gridPos[row][column][1] + HEIGHT:
                controller.cellClick(grid, row, column, livingCells)
    '''
    '''
    Instead of checking every single cell in grid, find the clicked cell by first finding the correct row then
    finding the correct column within that row.
    '''
    for row in range(blocksInCol):
        #look for correct row
        if clickPos[1] >= gridPos[row][0][1] and clickPos[1] <= gridPos[row][0][1] + HEIGHT:
            #found correct row, now look for column
            for column in range(blocksInRow):
                if clickPos[0] >= gridPos[row][column][0] and clickPos[0] <= gridPos[row][column][0] + WIDTH:
                    #found correct column
                    controller.cellClick(grid, row, column, livingCells)
def drawGrid():

    global dragVect

    surface.fill(BLACK)
    #oldDragVect = dragVect
    # Draw the grid
    for row in range(blocksInRow):
        for column in range(blocksInCol):

            color = BLACK
            if grid[row][column] == 0:
                color = GREEN
            elif grid[row][column] == 1:
                color = WHITE
            '''
            #Not being used because it creates distortion effect when grid is dragged.
            if row != 0 and column != 0:
                gridPos[row][column] = [gridPos[row][column - 1][0] + dragVect[0] + WIDTH + MARGIN,
                                        gridPos[row - 1][column][1] + dragVect[1] + HEIGHT + MARGIN]
            elif row != 0:
                gridPos[row][column] = [gridPos[row][column][0] + dragVect[0],
                                        gridPos[row - 1][column][1] + dragVect[1] + HEIGHT + MARGIN]
            elif column != 0:
                gridPos[row][column] = [gridPos[row][column - 1][0] + dragVect[0] + WIDTH + MARGIN,
                                        gridPos[row][column][1] + dragVect[1]]
            else:
                gridPos[row][column] = [(gridPos[row][column][0] + dragVect[0]),
                                    (gridPos[row][column][1] + dragVect[1])]
            '''
            '''
            The reason for splitting the two following sections instead of updating gridPos using just one of the two
            methods is that using solely the first method, with the if statements, creates a distortion effect when
            grid is dragged. However, using solely the second method neglects simulating zooms. Therefore, only one of
            the methods is used at any given time depending on whether the user dragged or zoomed. This assumes user
            cannot drag and zoom at the same time; a physically possible yet unlikely scenario due to the awkwardness
            of the action.
            '''
            #If no drag happened then no need to worry about simulating drag, rather focus on simulating potential zoom
            if dragVect == (0, 0):
                if row != 0 and column != 0:
                    gridPos[row][column] = [gridPos[row][column - 1][0] + WIDTH + MARGIN,
                                            gridPos[row - 1][column][1] + HEIGHT + MARGIN]
                elif row != 0:
                    gridPos[row][column] = [gridPos[row][column][0],
                                            gridPos[row - 1][column][1] + HEIGHT + MARGIN]
                elif column != 0:
                    gridPos[row][column] = [gridPos[row][column - 1][0] + WIDTH + MARGIN,
                                            gridPos[row][column][1]]
                else:
                    gridPos[row][column] = [(gridPos[row][column][0]),
                                        (gridPos[row][column][1])]
            else: #If drag did happen, then no need to simulate zoom, rather focus on simulating drag
                gridPos[row][column] = [(gridPos[row][column][0] + dragVect[0]),
                                        (gridPos[row][column][1] + dragVect[1])] #saves position of each cell in grid

            if row > (ommitedLines - 1) and row < (blocksInCol - ommitedLines) and column > (ommitedLines - 1) and column < (blocksInRow - ommitedLines):
                pygame.draw.rect(surface,
                                 color,
                                 [gridPos[row][column][0],
                                 gridPos[row][column][1],
                                 WIDTH,
                                 HEIGHT])
    #Prevents grid from sliding while mouse is pressed and cursor not moving.
    if lastMousePos == pygame.mouse.get_pos(): #This is probably true every frame due to "lastMousePos = event.pos"
        dragVect = (0, 0)

    currentTime = controller.formatTimeString(gameTimerhms)
    ren = font.render(currentTime, 0, RED, BLACK)
    surface.blit(ren, (0, 0))
    '''
    surface.blit(ren1, (10, 40), special_flags = 2)
    surface.blit(ren2, (10, 70), special_flags = 3)
    surface.blit(ren3, (10, 100), special_flags = 4)
    surface.blit(ren4, (10, 130), special_flags = 5)
    surface.blit(ren5, (10, 160), special_flags = 6)
    surface.blit(ren6, (10, 190), special_flags = 7)
    '''
    #surface.blit(ren, (10, 10), special_flags = 1)
    #print(gridPos)


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
    drawButtons(buttons)
    #drawButtons()
    # Handle user and system events
    for event in GAME_EVENTS.get():
        #Drags grid when right mouse button is pressed and held.
        if pygame.mouse.get_pressed()[2]: #This function is unreliable. Does not always return true even though mouse is still pressed.
                                          #When cursor is no longer moving, but mouse is still pressed, event.pos is ahead of lastMousePos.
                                          #However at this point the two values need to be the same as proven by lastMousePos = event.pos being printed last.
                                          #The reason is that even though the values are the same, the button press is not returning true anymore and thus
                                          #the old dragVect is the one being used. That's why we manually need to change dragVect when we realize that the
                                          #mouse hasn't moved since the last call.

            dragVect = (event.pos[0] - lastMousePos[0], event.pos[1] - lastMousePos[1])
            lastMousePos = event.pos

            #print("lastMousePos = event.pos")

        else:
            lastMousePos = pygame.mouse.get_pos() #Constanly updates lastMousePos variable to prevent snapping.
            #print("lastMousePos = pygame.mouse.get_pos()")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #scroll up
                #print("scrolled up")
                #print(HEIGHT)
                if WIDTH < maxZoomIn and HEIGHT < maxZoomIn: #maximum zoom in
                    oldWidth = WIDTH
                    oldHeight = HEIGHT
                    oldMargin = MARGIN
                    WIDTH += 1
                    HEIGHT += 1
                    #MARGIN = WIDTH * origMargin / origWidth #maintaining aspect ratio
                    #print(MARGIN)
            elif event.button == 5: #scroll down
                #print("scrolled down")
                #print(HEIGHT)
                if WIDTH > maxZoomOut and HEIGHT > maxZoomOut: #maximum zoom out
                    oldWidth = WIDTH
                    oldHeight = HEIGHT
                    oldMargin = MARGIN
                    WIDTH -= 1
                    HEIGHT -= 1
                    #MARGIN = WIDTH * origMargin / origWidth #maintaining aspect ratio
                    #print(MARGIN)
            elif event.button == 1:
                clickPos = pygame.mouse.get_pos()
                HandleClicks(clickPos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    clock.tick(60)
    pygame.display.update()