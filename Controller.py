#import View
'''

Next step: implement cell clicks. This will allow for configure to be activated and the pause/play button to have
functionality.
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
    if configured: #if player has activated some cells the game may be started
        if paused: #game will now be running
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

#def cellClick():
#    if paused:

