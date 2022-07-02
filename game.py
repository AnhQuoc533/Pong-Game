import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

FPS = 60
L_POS = -385  # Position of left paddle
R_POS = 375  # Position of right paddle
BORDER = 270
MAX_DIS = 15 + 10 * 26**(1/2)  # Maximum distance between ball and paddle
FORMAT = {'align': 'center', 'font': ("Courier", 20, "normal")}


class PongGame:

    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=795, height=630)
        self.screen.cv._rootwindow.resizable(False, False)  # Access Tkinter function from Canvas screen
        self.screen.title('Pong Game')
        self.screen.bgpic('gfx/bg.gif')
        self.screen.tracer(0)  # Turn off automatic screen update

        self.score = Scoreboard()
        self.ball = Ball()
        self.r_paddle = Paddle(R_POS)
        self.l_paddle = Paddle(L_POS)

        self.n_rounds = self.__get_nrounds()
        if self.n_rounds is None:
            self.screen.bye()
            return

        self.keys_pressed = {}  # Fix 2 players cannot move simultaneously
        self.__bind_key()

        self.is_paused = False
        self.__text = Turtle()
        self.__text.color('white')
        self.__text.hideturtle()
        self.__text.speed('fastest')
        self.__text.penup()
        self.__text.goto(0, -255)
        self.__text.write("Press 'Space' to pause the game.", **FORMAT)

    def __get_nrounds(self):
        title = 'How many rounds you want to play?'
        try:
            num = self.screen.numinput(title=title, prompt='Enter a number:', minval=1)
            while int(num) != num:
                num = self.screen.numinput(title=title, prompt='Invalid number, please try again:', minval=1)
            return num

        except TypeError:
            return None

    def __bind_key(self):
        self.screen.listen()
        self.screen.onkey(self.pause, 'space')  # Pause game

        keys = ['w', 's', 'W', 'S', 'Up', 'Down']
        functions = [self.l_paddle.up, self.l_paddle.down]*2 + [self.r_paddle.up, self.r_paddle.down]
        for key, function in zip(keys, functions):
            # Access Tkinter function from Canvas screen
            self.screen.cv.bind(f"<KeyPress-{key}>", self.__key_pressed)
            self.screen.cv.bind(f"<KeyRelease-{key}>", self.__key_released)
            self.keys_pressed[key] = [False, function]

    def __key_pressed(self, event):
        """Callback for KeyPress event listener and set key pressed state to True."""
        self.keys_pressed[event.keysym][0] = True

    def __key_released(self, event):
        """Callback for KeyRelease event listener and set key pressed state to False."""
        self.keys_pressed[event.keysym][0] = False

    def __change_text(self):
        if self.is_paused is None:
            self.__text.clear()
            self.__text.color('red')
            self.__text.goto(0, -20)
            self.__text.write('GAME OVER!', align='center', font=("Courier", 25, "bold"))

            # Restart game suggestion
            self.__text.color('white')
            self.__text.goto(0, -35)
            self.__text.write("Press 'Enter' to restart the game.", align='center', font=("Courier", 15, "normal"))

        elif self.is_paused:
            self.__text.clear()
            self.__text.write("Press 'Space' to continue the game.", **FORMAT)
            self.__text.goto(0, -15)
            self.__text.color('brown')
            self.__text.write("GAME PAUSED.", **FORMAT)

        else:
            for _ in range(4):
                self.__text.undo()
            self.__text.write("Press 'Space' to pause the game.", **FORMAT)

    def pause(self):
        if self.is_paused is not None:
            self.is_paused = not self.is_paused
            self.__change_text()

    def end(self):
        self.is_paused = None  # Block 'pause' text appearance after game is over
        self.__change_text()

    def reset(self):
        self.screen.clearscreen()
        self.__init__()

    def __ball_animation(self):
        if self.is_paused is False:
            self.ball.move()
            ball_xcor = self.ball.xcor()

            # Detect collision with wall
            if abs(self.ball.ycor()) > BORDER:
                self.ball.bounce(is_hit_border=True)

            # Ball is out of bound
            elif not (L_POS - 35 < ball_xcor < R_POS + 35):
                self.screen.update()
                time.sleep(0.5)
                winner = 0 if ball_xcor > 0 else 1
                self.score.increase_score(winner)

                # End game
                if self.score.l_score + self.score.r_score == self.n_rounds:
                    self.score.finalize()
                    self.end()
                    self.screen.onkey(self.reset, 'Return')  # 'enter' key

                # Restart the ball
                else:
                    self.ball.restart(winner)

            else:
                # Detect collision with right paddle
                ball_angle = self.ball.heading()
                if self.ball.distance(self.r_paddle) < MAX_DIS and R_POS - 25 < ball_xcor < R_POS and \
                        (self.ball.heading() < 90 or ball_angle > 270):
                    self.ball.bounce(is_hit_border=False)

                # Detect collision with left paddle
                elif self.ball.distance(self.l_paddle) < MAX_DIS and L_POS < ball_xcor < L_POS + 25 and \
                        (90 < ball_angle < 270):
                    self.ball.bounce(is_hit_border=False)

        self.screen.ontimer(self.__ball_animation, self.ball.move_speed)

    def __main_animation(self):
        if self.is_paused is False:
            self.screen.update()
            # Check state of key pressed and respond manually
            for value in self.keys_pressed.values():
                if value[0]:
                    value[1]()

        self.screen.ontimer(self.__main_animation, 1000//FPS)

    def play(self):
        if self.n_rounds:
            self.__ball_animation()
            self.__main_animation()
            self.screen.mainloop()


if __name__ == '__main__':
    PongGame().play()
