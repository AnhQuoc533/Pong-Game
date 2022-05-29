from turtle import Screen, Turtle
import time
from paddle import Paddle
from ball import Ball


class PongGame:

    def __init__(self):
        self.screen = Screen()
        self.screen.bgcolor('black')
        self.screen.setup(width=800, height=600)
        self.screen.title('Pong Game')
        self.screen.tracer(0)

        self.__ball = Ball()
        self.r_paddle = Paddle(375)
        self.l_paddle = Paddle(-385)
        self.__bind_key()
        self.speed = .08

    def __bind_key(self):
        self.screen.listen()
        self.screen.onkey(self.pause, 'Return')  # Pause game

        # Right paddle movement
        self.screen.onkeypress(self.r_paddle.up, 'Up')
        self.screen.onkeypress(self.r_paddle.down, 'Down')

        # Left paddle movement
        self.screen.onkeypress(self.l_paddle.up, 'w')
        self.screen.onkeypress(self.l_paddle.down, 's')
        # Capslock case
        self.screen.onkeypress(self.l_paddle.up, 'W')
        self.screen.onkeypress(self.l_paddle.down, 'S')

    def pause(self):
        ...

    def play(self):
        # self.screen.tracer(1)
        # t = Turtle()
        # t.pencolor('red')
        # t.goto(365, 280)
        # t.goto(365, -280)
        # t.goto(-375, -280)
        # t.goto(-375, 280)
        while True:
            self.screen.update()
            time.sleep(self.speed)
            self.__ball.move()

            # Detect collision with wall
            if abs(self.__ball.ycor()) > 280:
                self.__ball.bounce(is_hit_border=True)

            # Ball is out of bound
            ball_xcor = self.__ball.xcor()
            if abs(ball_xcor) > 420:
                time.sleep(1)
                self.__ball.restart()

            # Testing
            # if ball_xcor >= 350 or ball_xcor <= -360:
            #     print(ball_xcor)
            #     self.__ball.bounce(is_hit_border=False)

            # Detect collision with right paddle
            if self.__ball.distance(self.r_paddle) < 66 and ball_xcor > 350 and \
                    (self.__ball.heading() < 90 or self.__ball.heading() > 270):
                # For testing
                # print('right', ball_xcor)
                # print('right', self.__ball.distance(self.r_paddle))
                # time.sleep(1)
                self.__ball.bounce(is_hit_border=False)

            # Detect collision with left paddle
            elif self.__ball.distance(self.l_paddle) < 66 and ball_xcor < -360 and 90 < self.__ball.heading() < 270:
                # For testing
                # print('left', ball_xcor)
                # print('left', self.__ball.distance(self.l_paddle))
                # time.sleep(1)
                self.__ball.bounce(is_hit_border=False)


if __name__ == '__main__':
    PongGame().play()
