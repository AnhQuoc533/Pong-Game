import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball

L_POS = -385  # Position of left paddle
R_POS = 375  # Position of right paddle
BORDER = 270
MAX_DIS = 15 + 10 * 26 ** (1 / 2)  # Maximum distance between ball and paddle
FORMAT = {'align': 'center', 'font': ("Courier", 20)}


class Scoreboard(Turtle):
    format = {'align': 'center', 'font': ("Courier", 50, "bold")}

    def __init__(self):
        super().__init__()
        self.color('white')
        self.hideturtle()
        self.speed('fastest')
        self.penup()

        self.l_score = self.r_score = 0
        self.display_score()

    def display_score(self):
        self.clear()

        self.goto(-100, 210)
        self.write(self.l_score, **self.format)
        self.setx(100)
        self.write(self.r_score, **self.format)

    def increase_score(self, winner: int):
        # Left paddle win
        if winner == 0:
            self.l_score += 1

        # Right paddle win
        elif winner == 1:
            self.r_score += 1

        self.display_score()


class PongGame:

    def __init__(self):
        self.screen = Screen()
        self.screen.bgcolor('black')
        self.screen.setup(width=795, height=630)
        self.screen.cv._rootwindow.resizable(False, False)  # Access Tkinter function from Canvas screen
        self.screen.title('Pong Game')
        self.screen.bgpic('bg.gif')
        self.screen.tracer(0)

        self.score = Scoreboard()
        self.__ball = Ball()
        self.r_paddle = Paddle(R_POS)
        self.l_paddle = Paddle(L_POS)

        self.keys_pressed = {}  # Fix 2 players cannot move simultaneously
        self.__bind_key()

        self.is_paused = False
        self.__text = Turtle()
        self.__text.color('light salmon')
        self.__text.hideturtle()
        self.__text.speed('fastest')
        self.__text.penup()
        self.__text.goto(0, -255)
        self.__text.write("Press 'Enter' to pause the game.", **FORMAT)

    def __bind_key(self):
        self.screen.listen()
        self.screen.onkey(self.pause, 'Return')  # Pause game

        keys = ['w', 's', 'W', 'S', 'Up', 'Down']
        functions = [self.l_paddle.up, self.l_paddle.down] * 2 + [self.r_paddle.up, self.r_paddle.down]
        for key, function in zip(keys, functions):
            # Access Tkinter function from Canvas screen
            self.screen.cv.bind(f"<KeyPress-{key}>", self.__key_pressed)
            self.screen.cv.bind(f"<KeyRelease-{key}>", self.__key_released)
            self.keys_pressed[key] = [False, function]

    def __key_pressed(self, event):
        """ Callback for KeyPress event listener and set key pressed state to True."""
        self.keys_pressed[event.keysym][0] = True

    def __key_released(self, event):
        """ Callback for KeyRelease event listener and set key pressed state to False."""
        self.keys_pressed[event.keysym][0] = False

    def __change_text(self):
        if self.is_paused:
            self.__text.clear()
            self.__text.write("Press 'Enter' to continue the game.", **FORMAT)
            self.__text.goto(0, -20)
            self.__text.color('brown')
            self.__text.write("GAME PAUSED.", align='center', font=("Courier", 25, "bold"))

        else:
            for _ in range(4):
                self.__text.undo()
            self.__text.write("Press 'Enter' to pause the game.", **FORMAT)

    def pause(self):
        if self.__text is not None:
            self.is_paused = not self.is_paused
            self.__change_text()

    def play(self):
        # self.screen.tracer(1)  # For testing
        while True:
            self.screen.update()
            time.sleep(self.__ball.move_speed)

            if not self.is_paused:
                # Check state of key pressed and respond manually
                for value in self.keys_pressed.values():
                    if value[0]:
                        value[1]()

                self.__ball.move()

                # Detect collision with wall
                if abs(self.__ball.ycor()) > BORDER:
                    self.__ball.bounce(is_hit_border=True)

                # Ball is out of bound
                ball_xcor = self.__ball.xcor()
                if abs(ball_xcor) > 420:
                    winner = 0 if ball_xcor > 0 else 1
                    self.score.increase_score(winner)
                    self.__ball.restart(winner)

                    time.sleep(0.5)
                    self.screen.update()
                    time.sleep(1)
                    continue

                # Detect collision with right paddle
                ball_angle = self.__ball.heading()
                if self.__ball.distance(self.r_paddle) < MAX_DIS and 350 < ball_xcor < R_POS and \
                        (self.__ball.heading() < 90 or ball_angle > 270):
                    # For testing
                    # print('right', ball_xcor)
                    # print('right', self.__ball.distance(self.r_paddle))
                    # time.sleep(1)
                    self.__ball.bounce(is_hit_border=False)

                # Detect collision with left paddle
                elif self.__ball.distance(self.l_paddle) < MAX_DIS and L_POS < ball_xcor < -360 and \
                        (90 < ball_angle < 270):
                    # For testing
                    # print('left', ball_xcor)
                    # print('left', self.__ball.distance(self.l_paddle))
                    # time.sleep(1)
                    self.__ball.bounce(is_hit_border=False)


if __name__ == '__main__':
    PongGame().play()
