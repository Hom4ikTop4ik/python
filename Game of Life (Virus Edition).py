notes_line = """
        3 в ряд - асцелятор(2)
        4 в ряд - статичное
        5 в ряд - 4 * асцелятора "3 в ряд" (прицел как в кс)
        7 в ряд - 4 * "4 в ряд"
        8 в ряд - красивая анимация  +  4 * "4 в ряд"  +  4 * квадрата (2*2)
        9 в ряд - 2 * "5 в ряд"
        10 в ряд - асцилятор(15)
        11 в ряд - 2 * "3 в ряд"
        12 в ряд - 2 * "4 в ряд"
        14-15 в ряд - карсивая анимация, но потом ничего
        16 в ряд - мега прицел из кс // солнышко
        17 в ряд - 4 квадрата (2*2)
        """
notes = """
        2*2 - квадрат
        2*3 - статичное ("4 в ряд")
        2*9 - 2*асцилятора(2) ("11 в ряд")
        2*10 - 2*статичных ("12 в ряд")
        
        3*3 - "7 в ряд"
        3*8 - "10 в ряд"
        """

from graph import *
from PIL import Image
import math

from virus import virus
virus()

global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt, size

penSize(0)

fps = 25
time_update = int(1000/fps)

Pause_txt = text("Pause", 0, 0)
pause = True
press_LMB = False
press_RMB = False

k = 10 # scale (cell size)
size = [40, 40] # count cells in x, y (row and column)

cells = [[0 for y in range(size[1])] for x in range(size[0])]
brushColor("white")
cells_vis = [[rectangle(x*k, y*k, x*k+k-1, y*k+k-1) for y in range(size[1])] for x in range(size[0])]
neighbors_count = [[0 for y in range(size[1])] for x in range(size[0])]

canvasSize(size[0]*k, size[1]*k)

def mouse_down_LMB(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt 
    press_LMB = True

    x = event.x // k
    y = event.y // k

    if(cells[x][y] == 0):
        cells[x][y] = 1
        deleteObject(cells_vis[x][y])
        brushColor("black")
        cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)

def mouse_up_LMB(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt 
    press_LMB = False

def mouse_down_RMB(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt 
    press_RMB = True
    
    x = event.x // k
    y = event.y // k

    if(cells[x][y] == 1):
        cells[x][y] = 0
        deleteObject(cells_vis[x][y])

def mouse_up_RMB(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt 
    press_RMB = False

def mouse_down_MMB(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt 
    x = event.x // k
    y = event.y // k

    # inverting the cell
    cells[x][y] = 1 - cells[x][y]

    if(cells[x][y] == 0):
        deleteObject(cells_vis[x][y])
    if(cells[x][y] == 1):
        deleteObject(cells_vis[x][y])
        brushColor("black")
        cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)
    

def mouse_move(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt

    if(press_LMB or press_RMB):
        x = event.x // k
        y = event.y // k

        # if LMB is pressed, born the cell    
        if(press_LMB):
            if(cells[x][y] == 0):
                cells[x][y] = 1
                deleteObject(cells_vis[x][y])
                brushColor("black")
                cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)

        # if RMB is pressed, kill the cell    
        if(press_RMB):
            if(cells[x][y] == 1):
                cells[x][y] = 0
                deleteObject(cells_vis[x][y])

def keyPressed(event):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt, size

    if event.keycode == VK_SPACE:
        pause = not pause

    if event.keycode == VK_R:
        pause = True
        fill_random()

    if event.keycode == VK_Z:
        pause = True
        fill_zero()

    if event.keycode == VK_X:
        pause = True
        fill_one()

    if event.keycode == VK_Q:
        pause = True
        with Image.open("maps\\map.png") as img:
            # if img not GRAYSCALE   we make it so
            if( img.getbands() != ("L") ):
                gray_img = img.convert("L")
                gray_img.save('maps\\map.png')
        with Image.open("maps\\map.png") as img:
            img = img.resize(size)
            img.save("maps\\map.png")
            pix = img.load()
    
        for i in range(size[0]):
            for j in range(size[1]):
                if(pix[i,j]<200):
                    cells[i][j] = 1
                    deleteObject(cells_vis[i][j])
                    brushColor("black")
                    cells_vis[i][j] = rectangle(i*k, j*k, i*k+k-1, j*k+k-1)
                else:
                    cells[i][j] = 0
                    deleteObject(cells_vis[i][j])

    if event.keycode == VK_ESCAPE:
        close()


# counting the number of neighbors
def around_8(x, y):
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt

    summa = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i==0 and j==0):
                if(((x+i)>=0) and ((x+i)<size[0])  and  ((y+j>=0) and (y+j)<size[1])):
                    summa += cells[x+i][y+j]
    return summa

# will the cell be alive??
def B3_S23(n, alive): # number of neighbors, is alive?
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt

    # cell is born // remains alive
    if(n==3):
        return 1
    # cell remains alive
    elif(n==2 and alive):
        return 1
    # cell is dying
    return 0

def fill_one():
    for x in range(size[0]):
        for y in range(size[1]):
            if(cells[x][y] == 0):
                cells[x][y] = 1
                deleteObject(cells_vis[x][y])
                brushColor("black")
                cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)

def fill_zero():
    for x in range(size[0]):
        for y in range(size[1]):
            if(cells[x][y] == 1):
                cells[x][y] = 0
                deleteObject(cells_vis[x][y])

def fill_random():
    for x in range(size[0]):
        for y in range(size[1]):
            cells[x][y] = math.trunc(randint(0, 1))

            if(cells[x][y] == 0):
                deleteObject(cells_vis[x][y])
            if(cells[x][y] == 1):
                deleteObject(cells_vis[x][y])
                brushColor("black")
                cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)


def update():
    global cells, neighbors_count, pause, press_LMB, press_RMB, Pause_txt

    if(pause==False): # if game is active
        # delete text "Pause"
        deleteObject(Pause_txt)

        for x in range(size[0]):
            for y in range(size[1]):
                neighbors_count[x][y] = around_8(x, y)
        
        for x in range(size[0]):
            for y in range(size[1]):
                old = cells[x][y]
                new = B3_S23(neighbors_count[x][y], cells[x][y]==1)
                cells[x][y] = new

                # if burn >> died
                if(new == 0):
                    deleteObject(cells_vis[x][y])

                # if died >> burn
                if(new == 1):
                    deleteObject(cells_vis[x][y])
                    brushColor("black")
                    cells_vis[x][y] = rectangle(x*k, y*k, x*k+k-1, y*k+k-1)
    else:
        # create text "Pause"
        deleteObject(Pause_txt)
        Pause_txt = text("Pause", 0, 0)




onKey(keyPressed)                 # for keyboard press
onMouseDown(mouse_down_LMB, 1)    # for LMB press
onMouseUp(mouse_up_LMB, 1)        # for LMB unpress
onMouseDown(mouse_down_RMB, 3)    # for RMB press
onMouseUp(mouse_up_RMB, 3)        # for RMB unpress
onMouseDown(mouse_down_MMB, 2)    # for scrool / MMB press
onMouseMove(mouse_move)           # for mouse move

onTimer(update, time_update)      # eternal loop running with delay (I have fps limit)
run()                             # start game (visual)