from math import atan2, sqrt, pi

class DriveController:
    def __init__(self, bot):
        self.bot = bot

    def calculate_distance(self):
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

        return sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)

    def calculate_direction(self):
        delta_x = (
                self.bot.ball_location.x -
                self.bot.car_location.x
        )

        delta_y = (
                self.bot.ball_location.y -
                self.bot.car_location.y
        )

        return atan2(delta_y, delta_x)

    def calculate_relative_angle(self):
        direction = self.calculate_direction()

        relative_angle = direction - self.bot.car_orientation.yaw

        normalized_relative_angle = ((relative_angle + pi) % (2 * pi) - pi)

        return normalized_relative_angle

    def calculate_throttle(self, distance):
        v_max = 1410

        velocity = self.bot.car.physics.velocity

        speed = sqrt(velocity.x**2 + velocity.y**2)

        v_target = min(v_max, sqrt(2490 * distance))

        throttle = (v_target - speed) / v_max

        return max(-1.0, min(1.0, throttle))

    def use_handbrake(self, relative_angle):
        if abs(relative_angle) > pi / 4:
            return True
        else:
            return False

    def use_boost(self, distance, relative_angle):
        if (abs(relative_angle) <= pi / 8 and
                distance >= 1750 and
                self.bot.car.boost > 0 and
                self.bot.car.is_supersonic == False
        ):
            return True
        else:
            return False