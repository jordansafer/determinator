from Tkinter import *
import serialtest2
import thread
import time
import config
import pymsgbox  # pip install PsyMsgBox




# basic MVC animation setup with Tkinter
class DeterminatorAnimation(object):

    def __init__(self, width=300, height=300):
        config.new = False
        config.completed = True
        config.dataset = [] #List which stores EVERYONE'S data
        config.PersonName = ""
        config.collectingData = False
        (self.width, self.height) = (width, height)
        self.timerDelay = 250 # milliseconds, this delay between timer events

    def run(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack()

        #now start the animation sequence, create the model
        # (note nonstandard actions will be bound to the root here)
        self.initAnimation()

        # add actions
        self.root.bind("<Button-1>", lambda event: 
                                      self.onMousePressedWrapper(event))
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()

        # run the program
        self.root.mainloop()

    def onMousePressedWrapper(self, event):
        self.onMousePressed(event)
        self.redrawAll()

    def onKeyPressedWrapper(self, event):
        self.onKeyPressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):

        self.onTimerFired()
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)

    ################# Starting with the model ###
    def initAnimation(self):
        self.page = "start"
        self.initStart()
        self.initChooseUser()
        self.initLoading()
        self.initResults()

    ## start screen
    def initStart(self):
        (x, y) = (.5 * self.width, .6 * self.height)
        (dx, dy) = (.2 * self.width, .1 * self.height)
        (p1, p2) = self.getPoints((x, y), dx, dy)
        self.startButton = BetterButton(p1, p2, fill="#32B141",
            text="Start Recording", font = "arial 60 bold")

    ## user select screen
    def initChooseUser(self):
        (x, y) = (.25 * self.width, .4 * self.height)
        (dx, dy) = (.18 * self.width, .15 * self.height)
        (p1, p2) = self.getPoints((x, y), dx, dy)
        self.newButton = BetterButton(p1, p2, fill="#FFFBD0",
            text="New User", font = "arial 60 bold")
        (x, y) = (.75 * self.width, .4 * self.height)
        (dx, dy) = (.18 * self.width, .15 * self.height)
        (p1, p2) = self.getPoints((x, y), dx, dy)
        self.returnButton = BetterButton(p1, p2, fill="#FFFBD0",
            text="Returning User", font = "arial 60 bold")

    ## awaiting results screen
    def initLoading(self):
        pass

    ## results screen
    def initResults(self):
        (x, y) = (.85 * self.width, .85 * self.height)
        (dx, dy) = (.05 * self.width, .05 * self.height)
        (p1, p2) = self.getPoints((x, y), dx, dy)
        self.backButton = BetterButton(p1, p2, fill="#32B141",
            text="Return", font = "arial 20 bold")

    # finds corner points for a button based on its center and size
    def getPoints(self, center, deltaWidth, deltaHeight):
        x0 = center[0] - deltaWidth
        y0 = center[1] - deltaHeight
        x1 = center[0] + deltaWidth
        y1 = center[1] + deltaHeight
        return ((x0, y0), (x1, y1))


    ################ On to the view #############
    def redrawAll(self):
        self.canvas.delete(ALL)
        if self.page == "start":
            self.drawStart()
        elif self.page == "choose":
            self.drawChooseUser()
        elif self.page == "load":
            self.drawResults()
        elif self.page == "done":
            self.drawResults()

    ## start screen
    def drawStart(self):
        self.canvas.create_rectangle(0, 0, self.width/1.9, self.height,
                                                        fill = "blue")
        self.canvas.create_rectangle(self.width/2, 0, self.width, self.height,
                                                        fill = "red")
        self.canvas.create_text(self.width / 2, self.height / 4,
                    text = "The Determinator", font = "Georgia 100 bold")
        self.startButton.draw(self.canvas)

    ## user select screen
    def drawChooseUser(self):
        self.canvas.create_polygon(0,0, self.width, 0, 0, self.height,
                                                        fill = "#C13100")
        self.canvas.create_polygon(self.width, 0, 0, self.height,
                            self.width / 2, self.height, fill = "#FF9900")
        self.canvas.create_polygon(self.width, 0, self.width / 2, self.height,
                            self.width, self.height, fill = "#CC6600")
        self.newButton.draw(self.canvas)
        self.returnButton.draw(self.canvas)
        self.canvas.create_text(self.width / 2, self.height / 8,
            text = "Get ready to throw the ball.", font = "Impact 65")
        self.canvas.create_text(self.width / 2, self.height / 1.4,
            text = "\"Always channel your inner Peyton Manning\"",
            font = "Luminari 50")
        self.canvas.create_text(self.width / 2, self.height / 1.2,
            text = "-Peyton Manning", font = "Luminari 50")

    ## awaiting results screen
    def drawLoading(self):
        pass

    ## results screen
    def drawResults(self):
        self.backButton.draw(self.canvas)
        #self.canvas = Canvas(self.root, height=self.height, width=self.width)
        #backgroundImage = Tkinter.PhotoImage(file="blankedimage2.ppm")
        #backgroundLabel = Tkinter.Label(self.root,image=backgroundImage)
        #backgroundLabel.place(x=0,y=0)#,relWidth=1,relHeight=1)
        text = "Hello{0}. Throw to see your stats.".format(config.PersonName)
        self.canvas.create_text(self.width / 2, self.height * 1 / 8,
                        text = text , font = "Georgia 50 bold")
        power = "Rating: " + str(config.power_current) + "\t\tCurrent highscore: " \
                                        + str(config.power_highscore)
        self.canvas.create_text(self.width / 2, self.height * 2 / 8,
                        text = power, font = "Georgia 25")
        text2 = "Distance: " + str(config.distance_current) + " feet" + "\tCurrent distance highscore: "\
                                                + str(config.distance_highscore)
        self.canvas.create_text(self.width / 2, self.height * 3 / 8,
                        text = text2, font = "Georgia 25")
        hang = "Hangtime: " + str(config.hangtime_current) + " s" + "\tCurrent hangtime highscore: "\
                                                + str(config.hangtime_highscore)
        self.canvas.create_text(self.width / 2, self.height * 4 / 8,
                        text = hang, font = "Georgia 25")
        if config.power_current == config.power_highscore and config.power_highscore != 0:
            self.canvas.create_text(self.width / 2, self.height * 5 / 8,
                        text = "NEW POWER RATING HIGHSCORE!  \t" + str(config.power_highscore), font = "Georgia 25 bold")
        if config.distance_current == config.distance_highscore and config.distance_highscore != 0:
             self.canvas.create_text(self.width / 2, self.height * 6 / 8,
                        text = "NEW DISTANCE HIGHSCORE!  \t" + str(config.distance_highscore), font = "Georgia 25 bold")
        if config.hangtime_current == config.hangtime_highscore and config.hangtime_highscore != 0:
             self.canvas.create_text(self.width / 2, self.height * 7 / 8,
                        text = "NEW HANGTIME HIGHSCORE!  \t" + str(config.hangtime_highscore), font = "Georgia 25 bold")

    ################# Controller Time ############
    ## Mouse stuff ##
    def onMousePressed(self, event):
        if self.page == "start":
            self.clickStart(event)
        elif self.page == "choose":
            self.clickChooseUser(event)
        elif self.page == "load":
            self.clickResults(event)
        elif self.page == "done":
            self.clickResults(event)


    ## start screen logic
    def clickStart(self, event):
        if self.startButton.isClicked(event.x, event.y):
            # Launch thread from here
            self.page = "choose"
            thread.start_new_thread(serialtest2.makeReadings, (10, ))

    ## user select screen logic
    def clickChooseUser(self, event):
        if self.returnButton.isClicked(event.x, event.y):
            config.collectingData = True
            config.new = False
            config.completed = False
            self.page = "load"
        if self.newButton.isClicked(event.x, event.y):
            response = " " + pymsgbox.prompt('What is your name?')
            config.collectingData = True
            config.new = True
            config.PersonName = response # replace with function prompting user
            config.completed = False
            self.page = "load"

    ## results screen logic
    def clickResults(self, event):
        if self.backButton.isClicked(event.x, event.y):
            config.PersonName = ""
            self.page = "choose"


    ## KeyBoard stuff ############
    def onKeyPressed(self, event):
        if not self.page == "choose": return
        pass

    ## Timing stuff ############
    def onTimerFired(self):
        if not self.page == "load": return
        if(config.completed):
            print "finished"
            self.page = "done"
            config.CollectingData = False



# Button class for a button at a location with text and or color,
# 2.0 rendition now auto initializes values and allows for font changes
class BetterButton(object):

    # initializing a button for a designated screen location, with a color
    def __init__(self, point1, point2, text="", fill=None, font="arial 15"):
        self.clicked = False
        self.corner1 = point1
        self.corner2 = point2
        self.text = text
        self.font = font
        self.color = fill
        self.width = 0

    # the button draws itself on the canvas
    def draw(self, canvas):
        (p1, p2) = (self.corner1, self.corner2)
        text = self.text
        fill = self.color
        canvas.create_rectangle(p1, p2, fill = fill, width = self.width)
        midX = (p1[0] + p2[0]) / 2
        midY = (p1[1] + p2[1]) / 2
        canvas.create_text(midX, midY, text = text, font = self.font)

    # button returns if mouseclick is within its bounds
    def isClicked(self, x, y):
        (p1, p2) = (self.corner1, self.corner2)
        xCheck = p1[0] < x and x < p2[0]
        yCheck = p1[1] < y and y < p2[1]
        return xCheck and yCheck




DeterminatorAnimation(1400, 700).run()
