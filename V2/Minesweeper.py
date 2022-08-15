import Grid
import turtle

s = turtle.getscreen()
t = turtle.Turtle()
width = s.window_width();
height = s.window_height();
t.speed(1000000000)

def on_click(i, j):
    pass

s.onscreenclick(on_click)


resX = 10;
resY = 10;
sclX = width/resX
sclY = height/resY

for y in range(-resY//2, resY//2):
    for x in range(-resX//2, resX//2):
        ##region Color
        a = (x % 2 == 0)
        b = (y % 2 == 0)
        aNANDb = not(a and b)
        # (A NAND (A NAND B)) NAND (B NAND (A NAND B))
        if(a^b):
            t.fillcolor("black")
        else:
            t.fillcolor("white")
        ##endregion
        t.up()
        t.goto(x * sclX, y*sclY)
        t.down()
        t.begin_fill()
        t.goto((x + 1) * sclX, y * sclY)
        t.goto((x + 1) * sclX, (y + 1) * sclY)
        t.goto(x * sclX, (y + 1) * sclY)
        t.goto(x * sclX, y * sclY)
        t.end_fill()
