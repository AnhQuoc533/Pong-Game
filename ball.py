import turtle
import random


class Ball(turtle.Turtle):

    def __init__(self):
        self.ball_icons = []
        self.__add_icons()

        super().__init__(random.choice(self.ball_icons))
        self.penup()

        # For testing
        # self.ball_icons = ['arrow']
        # self.color('red')
        # self.speed('normal')

        starting_angle = random.randint(10, 350)
        while 80 < starting_angle < 100 or 170 < starting_angle < 190 or 260 < starting_angle < 280:
            starting_angle = random.randint(10, 350)

        self.setheading(starting_angle)

    def __add_icons(self):
        import os

        icons = os.listdir('ball')
        for icon in icons:
            ball_icon = 'ball/' + icon
            turtle.addshape(ball_icon)
            self.ball_icons.append(ball_icon)

    def move(self):
        self.forward(10)

    def bounce(self, is_hit_border: bool):
        # print('incidence:', self.heading())  # For testing
        if is_hit_border:
            self.setheading(360 - self.heading())
        else:
            self.setheading(180 - self.heading())
        # print('reflection:', self.heading())  # For testing

    def restart(self, winner: int):
        self.home()
        self.shape(random.choice(self.ball_icons))

        # Left paddle win
        if winner == 0:
            angle = random.randint(100, 260)
            while 170 < angle < 190:
                angle = random.randint(100, 260)
            self.setheading(angle)

        # Right paddle win
        elif winner == 1:
            angle = random.randint(280, 440)
            while 350 < angle < 370:
                angle = random.randint(100, 260)
            self.setheading(angle)
