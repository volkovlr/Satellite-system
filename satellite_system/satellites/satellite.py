import datetime

class Satellite:
    def __init__(
        self,
        view_angle: float,
        phase: float,
        reg_number: int,
        group_number: int,
        launch_date: datetime.datetime,
        state: str
    ):
        self.view_angle = view_angle
        self.reg_number = reg_number
        self.launch_date = launch_date
        self.state = state
