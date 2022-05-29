import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball

L_POS = -385  # Position of left paddle
R_POS = 375  # Position of right paddle
BORDER = 280
BALL_PADDLE = 66  # Minimum distance between ball and paddle
FORMAT = {'align': 'center', 'font': ("Courier", 20, "bold")}


class Scoreboard(Turtle):
    format = {'align': 'center', 'font': ("Courier", 40, "bold")}

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

        self.goto(-100, 200)
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
        self.screen.setup(width=800, height=600)
        self.screen.cv._rootwindow.resizable(False, False)  # Access Tkinter function from Canvas screen
        self.screen.title('Pong Game')
        self.screen.tracer(0)

        self.score = Scoreboard()
        self.__ball = Ball()
        self.r_paddle = Paddle(R_POS)
        self.l_paddle = Paddle(L_POS)
        self.speed = .02

        self.keys_pressed = {}  # Fix 2 players cannot move simultaneously
        self.__bind_key()

        self.is_paused = False
        self.__text = Turtle()
        self.__text.color('white')
        self.__text.hideturtle()
        self.__text.speed('fastest')
        self.__text.penup()
        self.__text.goto(0, -235)
        self.__text.write("Press 'space' to pause the game.", **FORMAT)

    def __bind_key(self):
        self.screen.listen()
        self.screen.onkey(self.pause, 'Return')  # Pause game

        for key in ['Up', 'Down', 'w', 's', 'W', 'S']:
            # Access Tkinter function from Canvas screen
            self.screen.cv.bind(f"<KeyPress-{key}>", self.__key_pressed)
            self.screen.cv.bind(f"<KeyRelease-{key}>", self.__key_released)
            self.keys_pressed[key] = False

    def __key_pressed(self, event):
        """ Callback for KeyPress event listener and set key pressed state to True."""
        self.keys_pressed[event.keysym] = True

    def __key_released(self, event):
        """ Callback for KeyRelease event listener and set key pressed state to False."""
        self.keys_pressed[event.keysym] = False

    def pause(self):
        self.is_paused = not self.is_paused

    def play(self):
        # self.screen.tracer(1)  # For testing
        while True:
            self.screen.update()
            time.sleep(self.speed)

            if not self.is_paused:
                # Check state of key pressed and respond manually
                if self.keys_pressed["w"]: self.l_paddle.up()
                if self.keys_pressed["s"]: self.l_paddle.down()
                if self.keys_pressed["W"]: self.l_paddle.up()
                if self.keys_pressed["S"]: self.l_paddle.down()
                if self.keys_pressed["Up"]: self.r_paddle.up()
                if self.keys_pressed["Down"]: self.r_paddle.down()

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
                    time.sleep(1)

                # Detect collision with right paddle
                ball_angle = self.__ball.heading()
                if self.__ball.distance(self.r_paddle) < BALL_PADDLE and 350 < ball_xcor < R_POS and \
                        (self.__ball.heading() < 90 or ball_angle > 270):
                    # For testing
                    # print('right', ball_xcor)
                    # print('right', self.__ball.distance(self.r_paddle))
                    # time.sleep(1)
                    self.__ball.bounce(is_hit_border=False)

                # Detect collision with left paddle
                elif self.__ball.distance(self.l_paddle) < BALL_PADDLE and L_POS < ball_xcor < -360 and \
                        (90 < ball_angle < 270):
                    # For testing
                    # print('left', ball_xcor)
                    # print('left', self.__ball.distance(self.l_paddle))
                    # time.sleep(1)
                    self.__ball.bounce(is_hit_border=False)


if __name__ == '__main__':
    PongGame().play()
