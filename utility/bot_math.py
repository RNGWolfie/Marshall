from math import atan2, sqrt

class BotMath:
    def __init__(self, bot):
        self.bot = bot

    def calculate_vertical_angle(self):
        delta_x = (
            self.bot.ball_location.x -
            self.bot.car_location.x
        )

        delta_y = (
            self.bot.ball_location.y -
            self.bot.car_location.y
        )

        delta_z = (
                self.bot.ball_location.z -
                self.bot.car_location.z
        )

        distance = sqrt(delta_x ** 2 + delta_y ** 2)

        return atan2(delta_z, distance)