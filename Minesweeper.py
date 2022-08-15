#############################
## Importing our libraries ##
#############################
from graphics import *                                                                              #John Zelle's Graphics.py library
from random import random as rng                                                                    #Importing Random.random as rng.


##########################
### "Global" Variables ###
##########################

cols = 10                                                                                           #How many rows will our program have
rows = 10                                                                                           #How many cols will our program have
scl = 25                                                                                            #How large are our squares be
margin = 10                                                                                         #How much space on each side of the board before the edge of the window.

win = None
points = []                                                                                         #Blank array to hold our points
closedSet = []                                                                                      #This will be an array to hold all the previously revealed spaces.
TotalBombs = 0                                                                                      #This will be an int to hold how many bombs are on the board in total
FlaggedBombs = 0    
bombChance = 0.1                                                                                    #To win this game, you need to flag all of the bombs.
flagButton = None                                                                                   #This button will be used to flag a bomb.

class Space:
    i = -1                                                                                          #Our "x" position. This will also be this objects index.
    j = -1                                                                                          #Our "y" position. This will also be this objects index.
    isBomb = False                                                                                  #If this square is a bomb, this will be true, otherwise, false
    isRevealed = False                                                                              #If this square is revealed
    isFlagged = False                                                                               #Am I currently flagged?
    bombedNeighbors = 0                                                                             #How many of our neighbors have bombs in their kitchens...
    rect = None                                                                                     #This will be the actual rectangle on the board

    def __init__(self, i, j, rect):                                                                 #This function will be called when a class is instantiated
        self.i = i                                                                                  #Set my own i to be the i I was givin                                                                    
        self.j = j                                                                                  #Set my own j to be the j I was givin     
        self.rect = rect                                                                            #Set my own rect to be the rect I was givin     
                     
    def reveal(self):                                                                             #Call this function to draw the square and change it's color, or to draw it's bomb count.
        if not self.isFlagged:                                                                      #Have I been flagged?
            if not self.isBomb:                                                                     #Am I a bomb?
                self.c = Text(Point((1 + self.i) * scl, (1 + self.j) * scl), "")                         #Create a text node. Calculate the centers of all of our points.
                if self.bombedNeighbors == 0:                                                       #If we have no bombed neighbors
                    self.rect.setFill("white")                                                      #Fill White
                else:                                                                               #Otherwise
                    self.c.setText(self.bombedNeighbors)                                                 #Set the text within our box to be the bomb count
                    self.c.draw(win)                                                                     #Put the text onto the board
                    self.rect.setFill("white")                                                      #Fill the spot white.
            else:
                self.rect.setFill(color_rgb(255, 0, 0))                                             #If we are a bomb, change our fill to red.
            self.isRevealed = True                                                                  #Let the class know that we have revealed this square.

    def flag(self):                                                                                 #This function will be called to flag the current square.
        if self.isFlagged:                                                                          #If we are already flagged
            self.rect.setFill("gray")                                                               #Temporarilly set the board's color at that space to gray
        else:                                                                                       #Otherwise
            self.rect.setFill("yellow")                                                             #Set the color to yellow.
        self.isFlagged = not self.isFlagged                                                         #Invert our "isFlagged" bool
        if self.isRevealed:                                                                         #If we have revealed this square before, reveal it again.
            self.reveal()

        
            

#Check where the mouse landed. Passes a point, where the mouse had clicked.
def checkSquare(MousePosition):
    x = MousePosition.getX()                                                                        #Get the X value out of our mouse point
    y = MousePosition.getY()                                                                        #Get the Y value out of our mouse point
    print(f"Click detected at: ({x}, {y})")                                                         #Tell the user that a click was indeed detected (Raw Value)
    if(x > margin and x < win.width - margin) and (y > margin and y < win.height - margin):         #If we clicked within the board
        i = int((x - margin)//scl)                                                                  #Calculate where the cursor ad clicked (X-Axis)
        j = int((y - margin)//scl)                                                                  #Calculate where the cursor had clicked (Y-Axis)
        return [i, j]                                                                               #Returns an array of points i and j.
    else:
        return None                                                                                 #If we didn't land in that point, return python's NULL value.

#Initialize our board
def init():
    global scl                                                                                  #Tell python that we are using the global variables scl, points, and totalbombs, not new local ones.
    global points
    global TotalBombs
    global win
    global bombChance
    global Welcome
    global flagButton
    Welcome.close()
    if win == None or not win.isOpen():
        #Create a window TITLE:         X:                          Y:
        win = GraphWin("Minesweeper", (cols * scl) + (2 * margin), (rows * scl) + (2 * margin) + 2*scl) 
    #try:                                                        
    for i in range(cols):                                                                       #
        points.append([""] * rows)                                                              #Append a new array to make this a 3d array. This was stolen from that javascript code.
    
    for y in reversed(range(rows)):                                                                       #for y = 0; y < rows; y++
        for x in reversed(range(cols)):                                                                   #for y = 0; y < rows; y++
            rect = Rectangle(                                                                   #
                Point(margin + (x * scl), margin + (y * scl)),                                  #
                Point(margin + (x * scl) + scl, margin + (y * scl) + scl)                       #Create a new rectangle which will be our grid square.
                )                                                                               #
            rect.setFill("gray")                                                                #Set the rectangle fill to be gray, and draw it to the screen
            rect.draw(win)                                                                      #Draw the rectangle
            points[x][y] = Space(x, y, rect)                                                    #Make an instance of our Space class, and put it at the boards x/y position and the board's rectangle spot..

    for i in range(cols):                                                                       #This is basically a foreach statement, but foreach doesn't exist in python, so we use a double loop.
        for j in range(rows):                                                                               
            if rng() <= bombChance:                                                                    #There is a 10% chance that this space will be a bomb... I used this number because it looked about right.
                points[i][j].isBomb = True                                                      #Set the bool isBomb to be true
                TotalBombs += 1                                                                 #Increment totalBombs by one.
        
    for i in range(cols):                                                                       #For i in cols
        for j in range(rows):                                                                   #For j in rows
            for dx in [-1, 0, 1]:                                                               #Iterate through all 3 x positions we can have as neighbors
                for dy in [-1, 0, 1]:                                                           #Iterate though all 3 y posistions we can have as neighbors
                    if ((i + dx >= 0 and i + dx <= rows - 1) 
                            and (j + dy >= 0 and j + dy <= cols - 1)):                          #Catch those edge cases!
                        if points[i+dx][j+dy].isBomb:                                           #If this space is a bomb
                            points[i][j].bombedNeighbors += 1                                   #Increment our bombed neighbor count by 1.
    flagButton = Rectangle(Point(margin, cols*scl + margin), Point(win.width - margin, win.height - margin))
    flagButton.setFill("yellow")
    flagButton.draw(win)
    flagButtonText = Text(Point((margin + win.width - margin) / 2, (cols*scl + margin + win.height - margin)/2), "Flag")
    flagButtonText.setSize(15)
    flagButtonText.draw(win)
                
    return True                                                                                 #This was initially used that if there was any error with setup, the program would crash with dignity, rather than yell.
    #except:                                                                                         #Reasons that this could happen include: closing the window before setup was done
        #return False                                                                                #If our setup crashes, then return false...
def gameOver(): #If the player hits a bomb:
    global win
    global points
    #win.close()
    GOWin = GraphWin("Game Over!")                                                                  #Create a window with the title of "Game Over", and a size of 200x200 (Default)
    GOText = Text(Point(100, 80), "Game Over")                                                      #Create a text node, centered at (100, 80), which says "Game Over"
    GOSubScript = Text(Point(100, 115), "You hit a bomb, and exploded!")                            #Create a text node, centered at (100, 115), which says "You hit a bomb, and exploded!"
    GOWin.setBackground("black")                                                                    #Set our window's background to be black
    GOText.setTextColor("white")                                                                    #Set the GameOver text to be white
    GOSubScript.setTextColor("white")                                                               #Set the "You hit a bomb..." text to be white
    GOText.setSize(20)                                                                              #Set our font sizes
    GOSubScript.setSize(13)                                                                         #Set our font sizes 2: Electric Boogaloo
    GOText.draw(GOWin)                                                                              #Draw our text
    GOSubScript.draw(GOWin)                                                                         #Same as above.
    

    
    Quit = Rectangle(Point(10, 130), Point(90, 190))                                               #Create a rectangle                
    Quit.setFill("Red")                                                                             #Make it red
    QText = Text(Point(50, 160), "Quit")                                                            #Make some text that says "Quit"
    Quit.draw(GOWin)                                                                                #Draw the Window
    QText.draw(GOWin)                                                                               #Draw the text
    
    PAgain = Rectangle(Point(100, 130), Point(190, 190))                                               #Create a rectangle                
    PAgain.setFill("Green")                                                                             #Make it red
    PText = Text(Point(140, 160), "Play Again")                                                            #Make some text that says "Quit"
    PAgain.draw(GOWin)                                                                                #Draw the Window
    PText.draw(GOWin)                                                                               #Draw the text
    
    
    MousePoint = GOWin.getMouse()                                                                   #Get the point of the next mouse clicl
    while (not(MousePoint.getX() > 100 and MousePoint.getX() < 190) and (MousePoint.getY() > 130)) and ((MousePoint.getY() < 190) and not(MousePoint.getX() > 10 and MousePoint.getX() < 90) and (MousePoint.getY() > 130 and MousePoint.getY() < 190)):
        MousePoint = GOWin.getMouse()                                                               #While we do not click in the box, keep getting mouse input.
    if (MousePoint.getX() > 10 and MousePoint.getX() < 90) and (MousePoint.getY() > 130 and MousePoint.getY() < 190): #If we click the "Quit" button, then                                                                                               #Close the main window
        GOWin.close()                                                                               #Close this window
        win.close()                                                                                 #Close the main window
    else:                                                                                           #Otherwise,
        GOWin.close()                                                                               #Close this window
        for i in range(rows):                                                                       #Undraw all of our squares
            for j in range(cols):
                points[i][j].rect.undraw()
                try:                                                                                #Try to undraw the label, however, some do not have labels assigned
                    points[i][j].c.undraw()
                except:                                                                             #If we get a NoneType error
                    True                                                                            #Then do nothing. Python doesn't have a no-op command, so I just said true, and that seems to work just fine.
                points[i][j] = None                                                                 #Set our point to be Null.

        gameStart()                                                                                 #Restart the game.

    
    
    
    
def WinScreen():                                                                                    #This function is called when the player wins!
    WinWin = GraphWin("Game Over!")                                                                 #Create a window with the title of "Winner!", and a size of 200x200 (Default)
    WinImg = Image(Point(100, 100), "Img/Winner.png")                                               #Create a image that was made in photoshop, and draw it to the board.
    WinImg.draw(WinWin)

    
    Quit = Rectangle(Point(10, 130), Point(90, 190))                                                #Create a rectangle                
    Quit.setFill("Red")                                                                             #Make it red
    QText = Text(Point(50, 160), "Quit")                                                            #Make some text that says "Quit"
    Quit.draw(WinWin)                                                                               #Draw the Window
    QText.draw(WinWin)                                                                              #Draw the text
    
    PAgain = Rectangle(Point(100, 130), Point(190, 190))                                            #Create a rectangle                
    PAgain.setFill("Green")                                                                         #Make it red
    PText = Text(Point(140, 160), "Play Again")                                                     #Make some text that says "Quit"
    PAgain.draw(WinWin)                                                                             #Draw the Window
    PText.draw(WinWin)                                                                              #Draw the text
    
    
    MousePoint = WinWin.getMouse()                                                                  #Get the point of the next mouse clicl
    while (not(MousePoint.getX() > 100 and MousePoint.getX() < 190) and (MousePoint.getY() > 130)) and ((MousePoint.getY() < 190) and not(MousePoint.getX() > 10 and MousePoint.getX() < 90) and (MousePoint.getY() > 130 and MousePoint.getY() < 190)):
        MousePoint = WinWin.getMouse()                                                              #While we do not click in the box, keep getting mouse input.
    if (MousePoint.getX() > 10 and MousePoint.getX() < 90) and (MousePoint.getY() > 130 and MousePoint.getY() < 190):                                                                                                #Close the main window
        WinWin.close()                                                                              #If we click the quit button
        win.close()                                                                                 #Close both windows
    else:                                                                                           #Otherwise
        WinWin.close()                                                                              #Close the win window
        for i in range(rows):                                                                       #Reset our variables again
            for j in range(cols):
                points[i][j].rect.undraw()
                try:
                    points[i][j].c.undraw()
                except:
                    True
                points[i][j] = None

        gameStart()                                                                                 #Go back to game start


def gameStart():
    
    global win

    global FlaggedBombs, TotalBombs, closedSet                                                      #Make sure we use the global variables
    closedSet = []                                                                                  #Set closedSet (Our already eval spots), to be empty

    TotalBombs = 0

    SetupResult = init()    

    FlaggedBombs = 0                                                                                #Set FlaggedBombs to be equal to zero.
    #print(SetupResult)
    if SetupResult:                                                                                 #If our setup didn't crash... I mean, it shouldn't, but you never know
        while True:                                                                                 #While true == true
            try:                                                                                    #If our user didn't cause the game to break,
                if(TotalBombs == FlaggedBombs):                                                         #If our user correctly flags each and every bomb, and no incorrect spaces
                    WinScreen()                                                                         #Load the win screen
                    break                                                                               #Break the loop.
                flagMode = False
                currentMouse = win.getMouse()                                                           #Get the current Mouse position
                while (currentMouse.getX() >= margin and currentMouse.getX() <= win.width-margin) and (currentMouse.getY() >= cols*scl + margin and currentMouse.getY() <= win.height - margin):  #Point(margin, cols*scl + margin), Point(win.width - margin, win.height - margin)
                    flagMode = True                                                                     #If we click within the "Flag" box, then set flag mode to true
                    currentMouse = win.getMouse()                                                       #Recapture our mouse.
                currentSquare = checkSquare(Point(currentMouse.getX(), currentMouse.getY()))            #Set CurrentSquare to be the array that we had created earlier [i, j]
                LastKey = win.checkKey()                                                                #Check to see what the latest key pressed was
                print(f"Mouse Click at: {currentMouse.getX()}, {currentMouse.getY()}, Square Position: {currentSquare[0]}, {currentSquare[1]}, Key Press: {LastKey}")
                #points[currentSquare[0]][currentSquare[1]].reveal()
                if points[currentSquare[0]][currentSquare[1]].bombedNeighbors == 0 and (LastKey != "f" or not flagMode):  #If we have no bombed neighbors at this space, and we do not intend to flag this space:
                    
                                                                                                        #I will be completely honest. I used wikipedia (https://en.wikipedia.org/wiki/Flood_fill#Moving_the_recursion_into_a_data_structure) to get a basis of how this algorhythm works
                                                                                                        #However, this is only pseudocode, and needed to be converted into Python, and to make sure it works.
                    Queue = []                                                                          #Create an empty array called Queue, which will hold all of our fill points.
                    Queue.append(currentSquare)                                                         #Append the current position to the Queue Array
                    while len(Queue) != 0:                                                              #While we still have points to check
                        n = Queue[0]                                                                    #Make n be the first item in the queue
                        print(n)
                        Queue.remove(n)                                                                 #Delete n from the array
                        if n in closedSet or points[n[0]][n[1]].isFlagged:                              #If n has already been evaluated, or n is currently flagged
                            continue                                                                    #Continue
                        points[n[0]][n[1]].reveal()                                                     #Otherwise, reveal this square
                        if points[n[0]][n[1]].bombedNeighbors == 0:                                     #If this point doesn't have any bombed neighbors
                            if n[0] < cols - 1:                                                         #Make sure we do not get an index out of range error
                                if points[n[0] + 1][n[1]] != None:                                      #Make sure that the point is not null
                                    Queue.append([n[0]+1, n[1]])                                        #Add the "south" neighbor of out square to the queue
                            if n[0] > 0:                                                                #Make sure we do not loop back to get the neighbor of (0, 0) to be (10, 10)
                                if points[n[0] - 1][n[1]] != None:                                      #Make sure that the point is not null
                                    Queue.append([n[0]-1, n[1]])                                        #Add the North Neighbor
                            if n[1] < rows - 1:                                                         #Make sure we do not get an index out of range error
                                if points[n[0]][n[1] + 1] != None:                                      #If our point is not null
                                    Queue.append([n[0], n[1] + 1])                                      #Add the east neighbor to the list
                            if n[1] > 0:                                                                #Make sure we don't underflow the index
                                if points[n[0]][n[1] - 1] != None:                                      #Make sure it is not null
                                    Queue.append([n[0], n[1] - 1])                                      #Add the west neighbor to the queue
                        closedSet.append(n)                                                             #Add our current point that we worked with to closedSet (evaluated spaces)
                elif LastKey == "f" or flagMode:                                                                    #If we intended to flag this spot
                    points[currentSquare[0]][currentSquare[1]].flag()                                   #Flag it
                    if points[currentSquare[0]][currentSquare[1]].isFlagged:                            #If the space is flagged
                        if points[currentSquare[0]][currentSquare[1]].isBomb:                           #And it is a bomb
                            FlaggedBombs += 1                                                           #Increment bombed spaces by one
                        else:                                                                           #Otherwise, if it is not a bomb
                            print("Flagged Space is not a bomb!")                                       #Alert through the terminal that the flagged space is not a bomb
                            FlaggedBombs -= 100                                                         #Decrement the Flagged Bombs int by 100, so that the user can not just flag all spaces and win.
                    else:                                                                               #Otherwise, if it is unflagged
                        if points[currentSquare[0]][currentSquare[1]].isBomb:                           #And it is a bomb
                            FlaggedBombs -= 1                                                           #Decrement bombed spaces by one
                        else:                                                                           #Otherwise, if it is not a bomb
                            print("Unflagged Space is not a bomb!")                                     #Alert the user that the unflagged space is not a bomb
                            FlaggedBombs += 100                                                         #Increment the flagged bomb int by 100
                                                                                
                elif points[currentSquare[0]][currentSquare[1]].isBomb:                                 #If the space is a bomb
                    if not points[currentSquare[0]][currentSquare[1]].isFlagged:                        #And if the space is not flagged
                        points[currentSquare[0]][currentSquare[1]].reveal()                             #Reveal the space
                        gameOver()                                                                      #Make it a game over
                        break                                                                           #and end the loop. :(
                else:                                                                                   #Finally, 
                    points[currentSquare[0]][currentSquare[1]].reveal()                                 #Reveal the current square
            except:                                                                                     #If they did try to break the program, or they clicked off grid,
                print("Space not valid!")                                                               #Carry on like nothing really happened.
    else:                                                                                           #Otherwise, break from the program.
        return 0
def Settings():                                                                                     #Make a settings box
    global rows, cols, scl                                                                          #Since we are changeing these variables, they need to be made globals!
    global bombChance                                                                               #Same with this one!

    SettingsImg = Image(Point(250, 250), "Img/Settings.png")                                        #Make the background of the window be another image made in photoshop
    SettingsImg.draw(Welcome)                                                                       #Draw it to the screen

    BombChance = Entry(Point(230, 195), 5)                                                          #Create a textbox
    BombChance.setSize(18)                                                                          #with font size 18
    BombChance.draw(Welcome)                                                                        #Draw it to the screen
    BombChance.setText(int(bombChance * 100))                                                       #Make the text be the percentage of bombs on the screen
    BombChance.setFill("white")                                                                     #Make the background white

    BoardSize = Entry(Point(230, 230), 5)                                                           #Create a textbox
    BoardSize.setSize(18)                                                                           #with font size 18
    BoardSize.setText(rows)                                                                         #Draw it to the screen
    BoardSize.draw(Welcome)                                                                         #Make the text be the percentage of bombs on the screen
    BoardSize.setFill("white")                                                                      #Make the background white

    SquareSize = Entry(Point(230, 265), 5)                                                          #Create a textbox
    SquareSize.setSize(18)                                                                          #with font size 18
    SquareSize.draw(Welcome)                                                                        #Draw it to the screen
    SquareSize.setText(scl)                                                                         #Make the text be the percentage of bombs on the screen
    SquareSize.setFill("white")                                                                     #Make the background white
    mousePos = Welcome.getMouse()                                                           
    while not ((mousePos.getX() > 330 and mousePos.getX() < 475) and (mousePos.getY() > 370 and mousePos.getY() < 440)):    #While our mouse is not in the continue box, 
        if (mousePos.getX() > 68 and mousePos.getX() < 182) and (mousePos.getY() > 85 and mousePos.getY() < 145):           #If we press the "Easy" button
            BombChance.setText("10")
            BoardSize.setText("10")
        if (mousePos.getX() > 194 and mousePos.getX() < 306) and (mousePos.getY() > 85 and mousePos.getY() < 145):          #If we press the "Medium" button
            BombChance.setText("25")
            BoardSize.setText("18")
        if (mousePos.getX() > 316 and mousePos.getX() < 430) and (mousePos.getY() > 85 and mousePos.getY() < 145):          #If we press the "Hard" button
            BombChance.setText("35")
            BoardSize.setText("30")
        mousePos = Welcome.getMouse()                                                                                       #Get our mouse position
    
    rows = int(BoardSize.getText())                                                                                         #Set our rows to be the board size
    cols = rows                                                                                                             #Make the board be a square
    scl = int(SquareSize.getText())                                                                                         #Set our scale to be what the user set it to
    bombChance = int(BombChance.getText()) / 100                                                                            #Set the bomb chance to be what the user asked divided by 100 to make it a percentage
    gameStart()                                                                                                             #Start the actual game


#This will open the welcome screen!
def game():
    #Create a global variable called Welcome
    global Welcome
    global points
    points = []
    Welcome = GraphWin("Minesweeper", 500, 500)                             #Make Welcome be a graphical window, titled Minesweeper, and a size of 500x500
    img = Image(Point(250, 250), "Img/MainMenu.png")                        #Make the back of the welcome window be an image made in photoshop, called MainMenu.png
    img.draw(Welcome)                                                       #Draw it to the screen
    
    mousePos = Welcome.getMouse()                                           #Get the mouse's click location in the window.
    #This while statement makes sure that The user had actually clicked in one of the 3 boxes. While they did not click it, get the mouse's position
    while not ((mousePos.getX() > 50 and mousePos.getX() < 450) and (mousePos.getY() > 100 and mousePos.getY() < 315)) and not ((mousePos.getX() > 50 and mousePos.getX() < 200) and (mousePos.getY() > 362 and mousePos.getY() < 448)) and not ((mousePos.getX() > 303 and mousePos.getX() < 450) and (mousePos.getY() > 350 and mousePos.getY() < 450)):        
        print(mousePos)
        mousePos = Welcome.getMouse()                                       #Get the new mouse point

    if (mousePos.getX() > 50 and mousePos.getX() < 450) and (mousePos.getY() > 100 and mousePos.getY() < 315):  #If the user clicked in the START box
        gameStart()
    elif ((mousePos.getX() > 50 and mousePos.getX() < 200) and (mousePos.getY() > 362 and mousePos.getY() < 448)):  #If the user clicked the settings button
        img.undraw()
        Settings()
    else:                                                                                                       #Otherwise, then close the window.
        Welcome.close()
        return ""
game()