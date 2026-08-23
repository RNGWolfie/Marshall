from rlbot.flat import GamePacket, ControllerState
from rlbot.managers.bot import Bot
from game_state import GameState
from math import sqrt, atan2, pi

class Marshall(Bot):
    def __init__(self):
        super().__init__()
        self.game_state = None
        self.ball_radius = 93.15
        self.field_x = 4096
        self.field_y = 5120

    def get_output(self, packet: GamePacket) -> ControllerState:
        controls = ControllerState()

        self.game_state = GameState(packet, self.index, self.field_info)

        self.ball_state()

        distance = self.calculate_distance()

        relative_angle = self.calculate_relative_angle()

        handbrake = self.use_handbrake(relative_angle)

        boost = self.use_boost(distance, relative_angle)

        steering = self.ball_tracking()

        controls.throttle = self.calculate_throttle(distance)

        controls.steer = steering

        controls.handbrake = handbrake

        controls.boost = boost

        print(self.game_state.opponent_goal)

        return controls

    def calculate_distance(self):
        delta_x = (
                self.game_state.ball_location.x -
                self.game_state.car_location.x
        )

        delta_y = (
                self.game_state.ball_location.y -
                self.game_state.car_location.y
        )

        delta_z = (
                self.game_state.ball_location.z -
                self.game_state.car_location.z
        )

        return sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)

    def calculate_direction(self):
        delta_x = (
                self.game_state.ball_location.x -
                self.game_state.car_location.x
        )

        delta_y = (
                self.game_state.ball_location.y -
                self.game_state.car_location.y
        )

        return atan2(delta_y, delta_x)

    def calculate_relative_angle(self):
        direction = self.calculate_direction()

        relative_angle = direction - self.game_state.car_orientation.yaw

        normalized_relative_angle = ((relative_angle + pi) % (2 * pi) - pi)

        return normalized_relative_angle

    def calculate_vertical_angle(self):
        delta_x = (
            self.game_state.ball_location.x -
            self.game_state.car_location.x
        )

        delta_y = (
            self.game_state.ball_location.y -
            self.game_state.car_location.y
        )

        delta_z = (
                self.game_state.ball_location.z -
                self.game_state.car_location.z
        )

        distance = sqrt(delta_x **2 + delta_y ** 2)

        return atan2(delta_z, distance)

    def calculate_throttle(self, distance):
        v_max = 1410

        velocity = self.game_state.car.physics.velocity

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
                self.game_state.car.boost > 0 and
                self.game_state.car.is_supersonic == False
        ):
            return True
        else:
            return False

    def ball_state(self):
        self.ball_in_air = False
        self.ball_on_wall = False

        if self.game_state.ball_location.z > 100:
            self.ball_in_air = True

        x = self.game_state.ball_location.x
        y = self.game_state.ball_location.y
        tolerance = 5

        if (
                abs(x - (self.field_x - self.ball_radius)) <= tolerance or
                abs(x - (-self.field_x + self.ball_radius)) <= tolerance or
                abs(y - (self.field_y - self.ball_radius)) <= tolerance or
                abs(y - (-self.field_y + self.ball_radius)) <= tolerance
        ):
            self.ball_on_wall = True

    def ball_tracking(self):
        relative_angle = self.calculate_relative_angle()

        if self.ball_on_wall:
            vertical_angle = self.calculate_vertical_angle()

            if vertical_angle > 0:
                ball_x = self.game_state.ball_location.x
                ball_y = self.game_state.ball_location.y

                car_x = self.game_state.car_location.x
                car_y = self.game_state.car_location.y

                wall_offset = 250

                if abs(ball_x) > abs(ball_y):
                    if ball_x > 0:
                        target_x = ball_x - wall_offset
                    else:
                        target_x = ball_x + wall_offset

                    target_y = ball_y

                else:
                    target_x = ball_x

                    if ball_y > 0:
                        target_y = ball_y - wall_offset
                    else:
                        target_y = ball_y + wall_offset

                delta_x = target_x - car_x
                delta_y = target_y - car_y

                direction = atan2(delta_y, delta_x)

                relative_angle = direction - self.game_state.car_orientation.yaw

                relative_angle = ((relative_angle + pi) % (2 * pi)) - pi

        else:
            ball = self.game_state.ball_location
            car = self.game_state.car_location

            distance = self.calculate_distance()

            # Far from the ball: chase it directly.
            if distance > 500:
                target_x = ball.x
                target_y = ball.y

            # Close to the ball: start positioning for the shot.
            else:
                target = self.scoring()

                if target is not None:
                    target_x, target_y = target
                else:
                    target_x = ball.x
                    target_y = ball.y

            delta_x = target_x - car.x
            delta_y = target_y - car.y

            direction = atan2(delta_y, delta_x)

            relative_angle = direction - self.game_state.car_orientation.yaw

            relative_angle = ((relative_angle + pi) % (2 * pi)) - pi

        return relative_angle / pi

    def scoring(self):
        ball = self.game_state.ball_location
        velocity = self.game_state.ball_velocity
        goal = self.game_state.opponent_goal.location

        goal_x = goal.x - ball.x
        goal_y = goal.y - ball.y
        goal_z = goal.z - ball.z

        distance = sqrt(goal_x ** 2 + goal_y ** 2)

        if distance == 0:
            return None

        goal_direction_x = goal_x / distance
        goal_direction_y = goal_y / distance

        target_distance = 300

        target_x = ball.x - goal_direction_x * target_distance
        target_y = ball.y - goal_direction_y * target_distance

        return target_x, target_y