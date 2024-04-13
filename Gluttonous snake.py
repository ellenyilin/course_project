##import the relevant modules
import turtle
import random
import time
from functools import partial

##set up default values
g_screen = None
g_snake = None
g_monster = None
g_food = None
g_snake_sz = 10
g_intro = None
g_keypressed = None
g_status = None
g_win = None
foodleft = 5
snakeStop = False

#define collide to keep track of snake collide with wall or itself
collide = False
k = None

##start time
startTime = 0
##initial contact
contact = 0
##prepare for food list
indexList = [0,1,2,3,4]
numberList = [1,2,3,4,5]

#snake head cordinates List
xList = []
yList = []
list1 =[]
for t in range(1,12+1):
    xList.append(20*t)
    xList.append(-20*t)
for j in range(1,10+1):
    yList.append(20*j)
for j in range(1,14+1):
    yList.append(-20*j)
    
#snake body coordinates list
bodyList = []

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial",16,"normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

def configurePlayArea():

    # motion border
    m = createTurtle(0,0,"","black")
    m.shapesize(25,25,5)
    m.goto(0,-40)  # shift down half the status

    # status border 
    s = createTurtle(0,0,"","black")
    s.shapesize(4,25,5)
    s.goto(0,250)  # shift up half the motion

    # introduction
    intro = createTurtle(-200,150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial",16,"normal"))
    
    #contacts
    global g_contact
    g_contact = createTurtle(-220,250)
    g_contact.hideturtle()
    g_contact.write('Contact: 0', font=("arial",15,"bold"))

    # statuses
    status = createTurtle(0,0,"","black")
    status.hideturtle()
    status.goto(100,s.ycor()) 

    # time
    global g_time
    g_time = createTurtle(-60, 250)
    g_time.hideturtle()
    g_time.write('Time: 0', font=("arial",15,"bold"))

    return intro, status

def configScreen():
    #set up the screen
    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake by Wang Yilin")
    s.setup(500+120, 500+120+80)
    s.mode("standard")
    return s

def createTurtle(x, y, color="red", border="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x,y)
    return t

def updateStatus():
    g_status.clear()   
    motiont = 'Motion: ' + str(g_keypressed)
    g_status.write(motiont, font=('arial',15,'bold'))
    g_screen.update()
 
def updateTime():
    global startTime
    vtime = 'Time: ' + str(int(time.time() - startTime))
    g_time.clear()
    g_time.write(vtime, font=("arial",15,"bold"))
    g_screen.update()
    if abs(g_snake.xcor() - g_monster.xcor()) < 20 and abs(g_snake.ycor() - g_monster.ycor()) < 20:
        return

def updateContact():
    global g_contact
    global contact
    g_contact.clear()
    g_contact.write('Contact: '+ str(contact), font=("arial",15,"bold"))
    g_screen.update()

def createFood():
    for i in range(5):        
        x = random.choice(xList)
        y = random.choice(yList)

        f = createTurtle(x,y-12)
        f.hideturtle()
        f.write(i+1, align='center',font=('Arial', 14, 'normal'))
        global list1
        list1.append(f)
    global a1,a2,a3,a4,a5
    a1,a2,a3,a4,a5 = list1[0],list1[1],list1[2],list1[3],list1[4]
    global dict1
    dict1 = {a1:True,a2:True,a3:True,a4:True,a5:True}
    return a1,a2,a3,a4,a5

def eatFood():
    global g_snake_sz
    global foodleft
    #try if the snake head touches the food
    for k in list1:
        if round(k.xcor()) == round(g_snake.xcor()) and round(k.ycor()+12)  == round(g_snake.ycor()):
            if dict1[k]:
                t = list1.index(k) + 1
                k.clear()
            ##if eaten food is in the list, then remove it
            try:
                indexList.remove(t-1)
                foodleft -= 1
                g_snake_sz += t
            except:
                None            
    return list1

def setSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        g_snake.setheading( HEADING_BY_KEY[key] )

def onArrowKeyPressed(key):
    global g_keypressed
    g_keypressed = key
    setSnakeHeading(key)
    updateStatus()

def onTimerFood():
    ##change existence in a random interval
    g_screen.ontimer(onTimerFood,1000*random.randint(5,10))
    print('onTimerFood')
    global list1
    ##food motion
    for i in indexList:
        ##half of the chance to disappear
        if random.choice([True, False]):
            list1[i].clear()
            dict1[list1[i]] = False
        ##another half to appear
        else:
            list1[i].write(i+1, align='center',font=('Arial', 14, 'normal'))
            dict1[list1[i]] = True

    g_screen.update()
    
def onTimerSnake():
    global snakeStop
    global g_monster
    global g_screen
    global bodyList
    global collide

    print('onTimerSnake')
    eatFood()
    #check whether the snake stops
    ##stop motion
    if snakeStop:
        
        g_screen.ontimer(onTimerSnake, 200)

    ###normal motion
    if not snakeStop:
        #game begins
        if g_keypressed == None and foodleft != 0:
            g_screen.ontimer(onTimerSnake, 200)
            return
            
        #win the game
        if foodleft == 0:
            g_win = createTurtle(g_snake.xcor()-60,g_snake.ycor()+40,'red','red')
            g_win.hideturtle()
            g_win.write('Winner!', font=("arial",15,"bold"))
            g_screen.update()
            return
        
        #game Over!!
        elif abs(g_snake.xcor() - g_monster.xcor()) < 20 and abs(g_snake.ycor() - g_monster.ycor()) < 20:
            g_win = createTurtle(g_snake.xcor()-60,g_snake.ycor()+40,'red','red')
            g_win.hideturtle()
            g_win.write('Game Over!', font=("arial",15,"bold"))
            g_screen.update()
            return

        # Clone the head as body
        ##when not snake does not collide with wall or itself
        if collide == False:
            g_snake.color(*COLOR_BODY)
            g_snake.stamp()
            g_snake.color(COLOR_HEAD)

        #### create a clone of the turtle object
        g_snake_clone = g_snake.clone()
        #### move the clone forward by 20 units
        g_snake_clone.hideturtle()
        now_x = round(g_snake_clone.xcor())
        now_y = round(g_snake_clone.ycor())
        global k
        k = [now_x,now_y]
        if k not in bodyList:
            bodyList.append(k)
        g_snake_clone.forward(20)

        # get the x-coordinate of the clone
        future_x = round(g_snake_clone.xcor())
        future_y = round(g_snake_clone.ycor())

        ##do not go outside of the assigned area
        if future_x < -240 or future_x > 240 or future_y > 200 or future_y < -280:
            collide = True
            g_screen.ontimer(onTimerSnake, 200)
            return

        #do not cross itself
        if [future_x,future_y] in bodyList:
            collide = True
            g_screen.ontimer(onTimerSnake, 200)
            return

        collide = False           
        # Advance snake
        g_snake.forward(20)

        # Shifting or extending the tail.
        while len(g_snake.stampItems) < g_snake_sz:
            g_snake.stamp()
    
        # Remove the last square on Shifting.
        if len(g_snake.stampItems) > g_snake_sz:
            g_snake.clearstamps(1)
        # keep track of the body coordinates (delete the old ones)
        if len(bodyList) > g_snake_sz+1:
            del bodyList[0]

        # updateTime()
        g_screen.update()
        g_screen.ontimer(onTimerSnake, 200)

##a function that switch snake's motion            
def snakePause():
    global snakeStop
    if snakeStop == False:
        snakeStop = True
    elif snakeStop == True:
        snakeStop = False

def onTimerMonster():
    ##use monster to keep track of time and the number of contacts
    updateTime()
    updateContact()
    if foodleft != 0:
        g_screen.ontimer(onTimerMonster, 1000)
        print('onTimerMonster')

    ##number of contact
    global contact
    for p in bodyList:
        if abs(p[0] - g_monster.xcor()) <= 20 and abs(p[1] - g_monster.ycor()) <= 20:
            contact += 1
    ##if snake head touch monster, game over
    if foodleft == 0 or abs(g_snake.xcor() - g_monster.xcor()) < 20 and abs(g_snake.ycor() - g_monster.ycor()) < 20:
        return
    ##set monster's direction
    if random.randint(0,1)==1:
        if g_monster.ycor()-g_snake.ycor() > 0:
            g_monster.setheading(270)
        elif g_snake.ycor()-g_monster.ycor() > 0:
            g_monster.setheading(90)
    else:
        if g_monster.xcor()-g_snake.xcor() > 0:
            g_monster.setheading(180)
        elif g_snake.xcor()-g_monster.xcor() > 0:
            g_monster.setheading(0)

    
    g_monster.forward(20)    
    g_screen.update()

def startGame(x,y):
    g_screen.onscreenclick(None)
    global startTime
    startTime = time.time()
    print(startTime)
    g_intro.clear()

    g_screen.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)

    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(onTimerFood,random.randint(5,10))
    return startTime

if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status = configurePlayArea()
    g_food = createFood()

    updateStatus()

    g_monster = createTurtle(-110,-110,"purple", "black")
    g_snake = createTurtle(0,0,"red", "black")

    g_screen.onscreenclick(startGame)

    g_screen.onkey(snakePause,'space')

    g_screen.update()
    g_screen.listen()
    
    g_screen.mainloop()