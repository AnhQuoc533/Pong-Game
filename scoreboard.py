from turtle import Turtle


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

    def finalize(self):
        ...
