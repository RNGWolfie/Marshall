class GameState:
    def __init__(self, packet, index, field_info):
        self.packet = packet
        self.index = index
        self.ball = packet.balls[0]
        self.car = packet.players[self.index]
        self.team = self.car.team
        self.ball_location = self.ball.physics.location
        self.ball_velocity = self.ball.physics.velocity
        self.car_location = self.car.physics.location
        self.car_orientation = self.car.physics.rotation
        self.opponent_goal = None

        for goal in field_info.goals:
            if goal.team_num != self.team:
                self.opponent_goal = goal
                break