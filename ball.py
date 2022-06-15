import turtle
import random
BALL_ICONS = [
    'ball/baseball.gif',
    'ball/basketball.gif',
    'ball/billiard.gif',
    'ball/dodgeball.gif',
    'ball/fireball.gif',
    'ball/football.gif',
    'ball/golf.gif',
    'ball/sun.gif',
    'ball/tennis.gif',
    'ball/volleyball.gif'
]
for icon in BALL_ICONS:
    turtle.addshape(icon)


class Ball(turtle.Turtle):

    def __init__(self):
        self.move_speed = 0.02

        super().__init__(random.choice(BALL_ICONS))
        self.penup()

        starting_angle = random.randint(10, 350)
        while 80 < starting_angle < 100 or 170 < starting_angle < 190 or 260 < starting_angle < 280:
            starting_angle = random.randint(10, 350)

        self.setheading(starting_angle)

    def move(self):
        self.forward(10)

    def bounce(self, is_hit_border: bool):
        # print('incidence:', self.heading())  # For testing
        if is_hit_border:
            self.setheading(360 - self.heading())
        else:
            self.setheading(180 - self.heading() + random.uniform(-5, 5))  # Make the reflection angle stochastic
            self.move_speed *= 0.95
        # print('reflection:', self.heading())  # For testing

    def restart(self, winner: int):
        self.home()
        self.move_speed = 0.02
        self.shape(random.choice(BALL_ICONS))

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
                angle = random.randint(280, 440)
            self.setheading(angle)
