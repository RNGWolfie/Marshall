from rlbot.flat import GamePacket, ControllerState
from rlbot.managers.bot import Bot
from controllers.drive import DriveController

class Marshall(Bot):
    def __init__(self):
        super().__init__()

        self.ball = None
        self.ball_location = None

        self.car = None
        self.car_location = None
        self.car_orientation = None

        self.drive = DriveController(self)

    def get_output(self, packet: GamePacket) -> ControllerState:
        controls = ControllerState()
        self.ball = packet.balls[0]
        self.ball_location = self.ball.physics.location

        self.car = packet.players[self.index]
        self.car_location = self.car.physics.location
        self.car_orientation = self.car.physics.rotation

        return controls