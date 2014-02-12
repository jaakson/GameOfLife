from random import choice
from time import sleep
from graphics import *
from math import floor

# Setup: board size, random value generator, create board and rectangles.

def size():
    """ Returns the size of the board."""
    return 16

def random_bit():
    """Returns a random value of True or False."""
    return choice([True,False])

def initiate():
    """Returns an initial (random) board and accompanying rectangles."""
    board = []
    for i in range(size()): # fills in the initial board.
        row = []
        for j in range(size()):
            row.append(random_bit())
        board.append(row)
        
    rectangles = []    
    for i in range(size()): # constructs initial rectangles.
        row = []
        for j in range(size()):
            row.append(Rectangle(Point(i,j),Point(i+1,j+1)))
        rectangles.append(row)
        
    return (board,rectangles)
    
# Graphical methods. Please note: I changed the colours in update_color
# because the grey used in the exercise appeared black on my computer.

def update_color(x,y,board,rectangles):
    """Sets color in rectangles[x][y] to correct value according to the
    status of its corresponding cell in board."""
    if (board[x][y]):
        rectangles[x][y].setFill("DarkRed")
    else:
        rectangles[x][y].setFill("DimGray")

def set_colors(board,rectangles):
    """Given a board, colours all rectangles accordingly."""
    for i in range(size()):
        for j in range(size()):
            update_color(i,j,board,rectangles)

def set_changed_colors(board,rectangles,changes):
    """Only updates the cell colour for changed states."""
    for cell in changes:
        [i,j] = cell
        update_color(i,j,board,rectangles)

def draw_cells(rectangles,window):
    """Draws rectangles' cells in the window."""
    for row in rectangles:
        for cell in row:
            cell.draw(window)

# General game components.

def living_neighbors(x,y,board):
    """ Counts the number of living neighbors of the cell in the given
    coordinate (x,y).  If either coordinate is on the edge, we wrap.
    Finally, we return the number of neighbors."""
    neighbors = 0

    top1 = board[(x-1)%size()][(y+1)%size()]
    top2 = board[x][(y+1)%size()]
    top3 = board[(x+1)%size()][(y+1)%size()]
    mid1 = board[(x-1)%size()][y]
    mid2 = board[(x+1)%size()][y]
    low1 = board[(x-1)%size()][(y-1)%size()]
    low2 = board[x][(y-1)%size()]
    low3 = board[(x+1)%size()][(y-1)%size()]

    list_of_neighbors = [top1,top2,top3,mid1,mid2,low1,low2,low3]

    for cell in list_of_neighbors:
        if cell == True:
            neighbors = neighbors + 1
    return neighbors

def change_list(board1,board2):
    """Takes in two boards and returns a list of coordinates for those
    cells which have switched state."""
    changes = []
    for i in range(size()):
        for j in range(size()):
            if board1[i][j] != board2[i][j]:
                changes.append([i,j])
    return(changes)

def iterate(board):
    """Does one iteration, returns the next generation of cells.
    Returns the tuple (living,new_board), where living is the number of
    live cells and board is a matrix of boolean values corresponding
    to the liveness of each cell."""
    new_board = [] 
    for i in range(size()): # generates a completely False board.
        row = []
        for j in range(size()):
            row.append(False)
        new_board.append(row)
        
    for i in range(size()): # living cells set to True; False otherwise.
        for j in range(size()):
            if board[i][j] == True:
                new_board[i][j] = (1 < living_neighbors(i,j,board) < 4)
            else:
                new_board[i][j] = (living_neighbors(i,j,board) == 3)               

    living = 0 # counts the living
    for i in range(size()):
        for j in range(size()):
            if new_board[i][j] == True:
                living = living + 1

    changes = change_list(new_board,board)
    return (living,new_board,changes)

# Oppgave 1's main method is mini_life():

def mini_life():
    """Simple version of Game of Life. Runs through life cycles in a
    16x16 grid. User kills process manually."""

    window = GraphWin("Game of Life: mini-edition",400,400)
    window.setCoords(0,0,size(),size())
    
    (base_board,rectangles) = initiate()
    set_colors(base_board,rectangles)
    draw_cells(rectangles,window)
    while True:
        (living,new_board,changes) = iterate(base_board)
        base_board = new_board
        set_changed_colors(base_board,rectangles,changes)
        sleep(0.4)

# Oppgave 2's main method is big_life(), will use the following:

def is_inside(button,point):
    """Returns True iff the point lies inside the button."""
    x_pt = point.getX()
    y_pt = point.getY()
    x_lo = button.getP1().getX()
    y_lo = button.getP1().getY()
    x_hi = button.getP2().getX()
    y_hi = button.getP2().getY()
    return (x_lo < x_pt < x_hi) and (y_lo < y_pt < y_hi)

def in_grid(point):
    """Yields True iff point is on the board (i.e., if user has clicked
    a cell.)"""
    x_pt = point.getX()
    y_pt = point.getY()
    lo = 0
    hi = size()
    return (lo <= x_pt <= hi) and (lo <= y_pt <= hi)


def big_life():
    """Full version of Game of Life. Starts with a randomized board.
    User can type a number of iterations in the Cycles field and START
    the game.  User can CLEAR, RANDOMIZE, LOAD or SAVE a board. Clicking
    on a cell switches its state. Use QUIT to exit."""
    
    window = GraphWin("Game of Life",500,600)
    window.setCoords(0,-3,size(),size())
    window.setBackground("white")

# We start by generating the iteration entry field, buttons and text.

    entry = Entry(Point(1,-0.5),5)
    entry.setText("13") # default value makes START usable immediately.
    entry_text = Text(Point(1,-1.2),"Cycles")
    entry.draw(window)
    entry_text.draw(window)

    y1 = -2.9 # these y-values are used with all buttons and their text.
    y2 = -0.1
    y3 = -2.5 

    st_pt1 = Point(1.76,y1)
    st_pt2 = Point(3.74,y2)
    start = Rectangle(st_pt1,st_pt2)
    start_text = Text(Point(2.75,y3),"START")
    start.setFill("MediumSeaGreen")
    start.setOutline("white")
    start.draw(window)
    start_text.draw(window)

    cl_pt1 = Point(3.76,y1)
    cl_pt2 = Point(5.74,y2)
    clear = Rectangle(cl_pt1,cl_pt2)
    clear_text = Text(Point(4.75,y3),"CLEAR")
    clear.setFill("DeepSkyBlue")
    clear.setOutline("white")
    clear.draw(window)
    clear_text.draw(window)

    ran_pt1 = Point(5.76,y1)
    ran_pt2 = Point(8.74,y2)
    randomize = Rectangle(ran_pt1,ran_pt2)
    random_text = Text(Point(7.25,y3),"RANDOMIZE")
    randomize.setFill("DarkOrchid")
    randomize.setOutline("white")
    randomize.draw(window)
    random_text.draw(window)

    ld_pt1 = Point(8.76,y1)
    ld_pt2 = Point(10.74,y2)
    load = Rectangle(ld_pt1,ld_pt2)
    load_text = Text(Point(9.75,y3),"LOAD")
    load.setFill("MediumVioletRed")
    load.setOutline("white")
    load.draw(window)
    load_text.draw(window)

    sv_pt1 = Point(10.76,y1)
    sv_pt2 = Point(13.74,y2)
    save = Rectangle(sv_pt1,sv_pt2)
    save_text = Text(Point(12.25,y3),"SAVE")
    save.setFill("Gold")
    save.setOutline("white")
    save.draw(window)
    save_text.draw(window)

    gb_pt1 = Point(13.76,y1)
    gb_pt2 = Point(16,y2)
    goodbye = Rectangle(gb_pt1,gb_pt2)
    bye_text = Text(Point(14.875,y3),"QUIT")
    goodbye.setFill("FireBrick")
    goodbye.setOutline("white")
    goodbye.draw(window)
    bye_text.draw(window)


# We then get an initial board for the Game of Life:
    (base_board,rectangles) = initiate()
    set_colors(base_board,rectangles)
    draw_cells(rectangles,window)
    go_on = True

# Users can now click the buttons.
    while go_on == True:
        click = window.getMouse()

        if is_inside(start,click):
            iterations_text = entry.getText()
            iterations = eval(iterations_text)
            for cycles in range(iterations):
                (live,new_board,changes) = iterate(base_board)
                base_board = new_board
                set_changed_colors(base_board,rectangles,changes)
                sleep(0.4)

        elif is_inside(clear,click):
            cleared_board = []
            for i in range(size()):
                row = []
                for j in range(size()):
                    row.append(False)
                cleared_board.append(row)
            changes = change_list(cleared_board,base_board)
            base_board = cleared_board
            set_changed_colors(base_board,rectangles,changes)

        elif is_inside(randomize,click):
            (random_board,new_rectangles) = initiate()
            changes = change_list(random_board,base_board)
            base_board = random_board
            set_changed_colors(base_board,rectangles,changes)

# Note: loaded/saved boards are txt files containing rows of True/False.
        elif is_inside(load,click):
            filename = input("Please choose the file to load: ")
            file = open(filename,"r")
            print("Building new board...")
            loaded_board = []
            for text_row in file.readlines():
                row = []
                states = text_row.split()
                for state in states:
                    row.append(eval(state))
                loaded_board.append(row)
            changes = change_list(loaded_board,base_board)
            base_board = loaded_board
            set_changed_colors(base_board,rectangles,changes)
            print("Board loaded.")
            file.close()

        elif is_inside(save,click):
            filename = input("Please provide a filename: ")
            file = open(filename,"w")
            print("Writing to file...")
            for row in base_board:
                line = ""
                for value in range(size()):
                    line = line+str(row[value])+" "
                line = line+"\n"
                file.write(line)
            print("Wrote to file.")
            file.close()

        elif is_inside(goodbye,click):
            go_on = False
            window.close()

        elif in_grid(click):
            x = floor(click.getX())
            y = floor(click.getY())
            base_board[x][y] = not base_board[x][y]
            changed_cell = [x,y]
            set_changed_colors(base_board,rectangles,[changed_cell])
