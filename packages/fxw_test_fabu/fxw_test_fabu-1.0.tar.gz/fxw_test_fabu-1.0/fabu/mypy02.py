import turtle
'''
my_colors = ("red","green","yellow","black")

t.width(4)
t.speed(9)
for i in range(10):
    t.penup()
    t.goto(0,-i*10)
    t.pendown()
    t.color(my_colors[i%len(my_colors)])
    t.circle(15+i*10)
'''
width = 30
num = 18
x1 = [(-400,400),(-400+width*num,400)]
y1 = [(-400,400),(-400,400-width*num)]
t = turtle.Pen()
t.speed(10)

for i in range(0,19):
    t.penup()
    t.goto(x1[0][0],x1[0][1]-width*i)
    t.pendown()
    t.goto(x1[1][0],x1[1][1]-width*i)

for i in range(0,19):
    t.penup()
    t.goto(y1[0][0]+width*i,y1[0][1])
    t.pendown()
    t.goto(y1[1][0]+width*i,y1[1][1])
t.hideturtle()
turtle.done()