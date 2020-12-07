class Member():
    name = ""
    score = 0
    days = {}
    last_star_ts = float("inf")
    def __init__(self, name, score, days, last_star_ts):
        self.name = name
        self.score = score
        self.days = days
        self.last_star_ts = last_star_ts

class Day():
    part1 = 0
    part2 = 0

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "p1:{0} p2:{1}".format(self.part1, self.part2)

    def __repr__(self):
        return self.__str__()
