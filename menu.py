from tkinter import *
import pickle
import snake


def getScoresFromFile():
    """Gets high scores from file."""
    try:
        file = open("highscores.dat", "rb")
    except:  # If no file found, one is created with None Elements
        print("no scores yet")
        file = open("highscores.dat", "wb")
        for i in range(3):
            size = None
            pickle.dump(size, file)
        file.close()
        file = open("highscores.dat", "rb")
    small = pickle.load(file)
    normal = pickle.load(file)
    large = pickle.load(file)
    file.close()
    return small, normal, large


def showHighScoreScreen():
    """Shows high score screen."""
    for item in titleWidgets:  # Removes title screen widgets
        item.pack_forget()

    small, normal, large = getScoresFromFile()
    scoreLists = (small, normal, large)

    count = 0
    for size in scoreLists:  # Inserts Score lists into widgets
        scoreString = "No Scores Found...\n"
        if size:
            scoreString = ""
            for score, name in size:
                scoreString += name + ": " + str(score) + "\n"
        if count == 0:
            smallTxt.insert('0.0', scoreString)
        elif count == 1:
            normalTxt.insert('0.0', scoreString)
        else:
            largeTxt.insert('0.0', scoreString)
        count += 1

    # Centering Text
    smallTxt.tag_add("center", "1.0", "end")
    normalTxt.tag_add("center", "1.0", "end")
    largeTxt.tag_add("center", "1.0", "end")

    # Placing widgets
    smallTxt.place(anchor='nw', height='400', width='200', x='50', y='100')
    normalTxt.place(anchor='n', height='400', width='200', x='400', y='100')
    largeTxt.place(anchor='ne', height='400', width='200', x='750', y='100')
    okBtn.configure(command=lambda: backToTitleScreen("high"))
    okBtn.place(anchor='center', x='400', y='550')
    smallLabel.place(anchor='center', x='150', y='85')
    normalLabel.place(anchor='center', x='400', y='85')
    largeLabel.place(anchor='center', x='650', y='85')
    highScoresLabel.place(anchor='center', x='400', y='40')


def showAddScoreScreen(score, tileSize):
    """Shows add score screen."""
    scoreTxt.insert("0.0", score)  # Attaches score
    scoreTxt.tag_add("center", "1.0", "end")  # Centers Text
    scoreTxt.configure(state="disabled")  # Disables state
    nameInput.delete(0, "end")  # Clears texts from input box
    addScoreBtn.configure(command=lambda: addScore(score, tileSize))
    for item in addScoreWidgets:  # Shows add score screen widgets
        item.pack()


def addScore(score, tileSize):
    """Adds new score to correct high score list."""
    # Checks name is legal
    name = nameInput.get()
    if not name:
        return
    if len(name) > 9:
        return

    small, normal, large = getScoresFromFile()

    # Attaches or appends new score to correct list
    if tileSize == 10:
        if small:
            small += [(score, name)]
        else:
            small = [(score, name)]
    elif tileSize == 20:
        if normal:
            normal += [(score, name)]
        else:
            normal = [(score, name)]
    else:
        if large:
            large += [(score, name)]
        else:
            large = [(score, name)]

    scoreLists = (small, normal, large)
    appendScoresToFile(scoreLists)
    backToTitleScreen("add")


def appendScoresToFile(scoreLists):
    """Sorts, trims and adds new scores to file."""
    file = open("highscores.dat", "wb")
    for list in scoreLists:
        if list:
            list.sort(reverse=True)  # Sorts scores highest first
            list = list[:16]  # Trims scores down to not overflow text widget
        pickle.dump(list, file)
    file.close()


def backToTitleScreen(key=""):
    """Brings back the title screen and uses a key to determine which screen widgets to remove."""
    if key == "high":  # Removes widgets from High Score Screen
        for item in highScoreWidgets:
            item.place_forget()
        # Removes Text from Boxes
        smallTxt.delete("1.0", "end")
        normalTxt.delete("1.0", "end")
        largeTxt.delete("1.0", "end")
    elif key == "add":  # Removes widgets from Add Score Screen
        for item in addScoreWidgets:
            item.pack_forget()
        # Removes Text from Boxes
        scoreTxt.configure(state="normal")  # enables state needed for changing text?
        scoreTxt.delete("1.0", "end")

    for item in titleWidgets:  # Adds title screen widgets
        item.pack()
    normalRadio.select()  # Preemptively selects normal radio button size option


def startGame():
    """Starts the game of snake."""
    # Remove title widgets
    for item in titleWidgets:
        item.pack_forget()
    # Starts game
    canvas.pack()
    score = snake.play(root, canvas, tileSize.get(), width, height)
    canvas.pack_forget()
    showAddScoreScreen(score, tileSize.get())


# Instantiates window and widgets
root = Tk()
root.title("Snake")
root.resizable(False, False)
# VARIABLES
width = 800
height = 600
tileSize = IntVar(root, 20)
###################
root.minsize(width=width, height=height)
canvas = Canvas(bg='gray', width=width, height=height)

# Title Screen Widgets
title = Message(root, font="{Alien Encounters} 48 {bold}", justify='center', width="300", padx='100', pady='100',
                text="Snake")
startBtn = Button(root, text="Start", fg="Red", command=startGame, width="20", height="2")
scoreBtn = Button(root, text="High Scores", fg="Red", command=showHighScoreScreen, width="20", height="2")
smallRadio = Radiobutton(root, indicatoron="false", state="normal", text="Small", width="10", value="10",
                         variable=tileSize)
normalRadio = Radiobutton(root, indicatoron="false", state="normal", text="Normal", width="10", value="20",
                          variable=tileSize)
largeRadio = Radiobutton(root, indicatoron="false", state="normal", text="Large", width="10", value="50",
                         variable=tileSize)

# High Score Screen Widgets
smallTxt = Text(root, font='{Arial} 16')
normalTxt = Text(root, font='{Arial} 16')
largeTxt = Text(root, font='{Arial} 16')
okBtn = Button(root, text="OK", width="10")
smallLabel = Label(root, text="Small")
normalLabel = Label(root, text="Normal")
largeLabel = Label(root, text="Large")
highScoresLabel = Label(font='{Alien Encounters} 48 {bold}', text='High Scores')
# Tags for centering Text
smallTxt.tag_configure("center", justify='center')
normalTxt.tag_configure("center", justify='center')
largeTxt.tag_configure("center", justify='center')

# Add Score Screen Widgets
addScoresLabel = Message(root, font="{Alien Encounters} 48 {bold}", justify='center', width="300", padx='100',
                         pady='100', text="New Score")
scoreLabel = Label(root, text="Score:")
nameLabel = Label(root, text="Name:")
scoreTxt = Text(root, font='{Arial} 16', width="10", height="1")
scoreTxt.tag_configure("center", justify='center')
nameInput = Entry(root, font='{Arial} 16', width="10", justify='center')
addScoreBtn = Button(root, text="OK", width="10")
exitBtn = Button(root, text="Exit", width="10", command=lambda: backToTitleScreen("add"))

# Tuples of Screen Widgets
addScoreWidgets = (addScoresLabel, scoreLabel, scoreTxt, nameLabel, nameInput, addScoreBtn, exitBtn)
titleWidgets = (title, startBtn, scoreBtn, smallRadio, normalRadio, largeRadio)
highScoreWidgets = (smallTxt, normalTxt, largeTxt, okBtn, smallLabel, normalLabel, largeLabel, highScoresLabel)

backToTitleScreen()  # Brings up title screen
root.mainloop()
