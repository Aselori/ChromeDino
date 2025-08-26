class DayNightCycle:
    def __init__(self):
        self.is_night = False
        self.cycle_points = 1000

    def update(self, score):
        self.is_night = (score % (2 * self.cycle_points)) >= self.cycle_points

    def get_bg_color(self):
        return (40, 40, 60) if self.is_night else (245, 245, 245)
