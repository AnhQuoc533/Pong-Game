import turtle
import random
import playsound
import threading
MAX_SPEED = 2
BALL_ICONS = [
    'gfx/baseball.gif',
    'gfx/basketball.gif',
    'gfx/billiard.gif',
    'gfx/dodgeball.gif',
    'gfx/fireball.gif',
    'gfx/football.gif',
    'gfx/golf.gif',
    'gfx/sun.gif',
    'gfx/tennis.gif',
    'gfx/volleyball.gif',
    'gfx/pea.gif'
]
for icon in BALL_ICONS:
    turtle.addshape(icon)


class Ball(turtle.Turtle):

    def __init__(self):
        self.move_speed = 20  # Milliseconds

        super().__init__(random.choice(BALL_ICONS))
        self.penup()

        starting_angle = random.randint(10, 350)
        while 70 < starting_angle < 110 or 170 < starting_angle < 190 or 250 < starting_angle < 290:
            starting_angle = random.randint(10, 350)

        self.setheading(starting_angle)

    def move(self):
        self.forward(8)
        if self.move_speed > 20:
            self.move_speed = 20

    def bounce(self, is_hit_border: bool):
        # def bounce_sfx():
        #     try:
        #         playsound.playsound('sfx/bounce.wav', block=False)
        #     except playsound.PlaysoundException:
        #         pass
        #
        # threading.Thread(target=bounce_sfx, daemon=True).start()
        # print('incidence:', self.heading())  # Debugging
        if is_hit_border:
            self.setheading(360 - self.heading())
        else:
            self.setheading(180 - self.heading())
            if self.move_speed > MAX_SPEED:
                self.move_speed -= 1
                # print(self.move_speed)  # Debugging
        # print('reflection:', self.heading())  # Debugging

    def restart(self, winner: int):
        self.move_speed = 1000
        self.home()
        self.shape(random.choice(BALL_ICONS))

        # Left paddle win
        if winner == 0:
            angle = random.randint(110, 250)
            while 170 < angle < 190:
                angle = random.randint(110, 250)
            self.setheading(angle)

        # Right paddle win
        elif winner == 1:
            angle = random.randint(290, 430)
            while 350 < angle < 370:
                angle = random.randint(290, 430)
            self.setheading(angle)
