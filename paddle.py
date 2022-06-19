from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, x_cor):
        super().__init__('square')
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.color('white')
        self.speed('fastest')
        self.goto(x_cor, 0)

    def up(self):
        if (yaxis := self.ycor()) < 240:
            self.sety(yaxis + 10)

    def down(self):
        if (yaxis := self.ycor()) > -240:
            self.sety(yaxis - 10)
