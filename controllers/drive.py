from math import pi
from utility import bot_math

class DriveController:
    def __init__(self, bot):
        self.bot = bot

    def calculate_relative_angle(self):
        direction = bot_math.calculate_direction(
            self.bot.car_location,
            self.bot.ball_location
        )

        relative_angle = direction - self.bot.car_orientation.yaw

        return bot_math.normalize_angle(relative_angle)

    def calculate_throttle(self, distance):
        v_max = 1410

        speed = bot_math.calculate_speed(
            self.bot.car.physics.velocity
        )

        v_target = min(v_max, (2490 * distance) ** 0.5)

        throttle = (v_target - speed) / v_max

        return max(-1.0, min(1.0, throttle))

    def use_handbrake(self, relative_angle):
        return abs(relative_angle) > pi / 4

    def use_boost(self, distance, relative_angle):
        return (
            abs(relative_angle) <= pi / 8
            and distance >= 1750
            and self.bot.car.boost > 0
            and not self.bot.car.is_supersonic
        )