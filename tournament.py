# TODO: Create Tournament class
# Needs these attributes based on your JSON:
# - name
# - pts (points awarded)
# - participants (draw size)
# - slam (boolean)
# - surface
# - week

class Tournament:
    def __init__(self, name, pts, participants, slam, surface, week, country):
        self.name = name
        self.pts = pts
        self.participants = participants
        self.slam = slam
        self.surface = surface
        self.week = week
        self.country = country
