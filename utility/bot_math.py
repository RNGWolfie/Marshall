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

    def calculate_distance(self, a, b):
        delta_x = b.x - a.x
        delta_y = b.y - a.y
        delta_z = b.z - a.z

        return sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)

    def calculate_direction(self, a, b):
        delta_x = b.x - a.x
        delta_y = b.y - a.y

        return atan2(delta_y, delta_x)

    def normalize_angle(self, angle):
        from math import pi

        return (angle + pi) % (2 * pi) - pi

    def calculate_speed(self, velocity):
        return sqrt(velocity.x ** 2 + velocity.y ** 2)