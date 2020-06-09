from dataclasses import dataclass, field

@dataclass
class Pattern:
    x: int
    y: int
    blinker: dict = field(init=False)
    glider: dict = field(init=False)
    beacon: dict = field(init=False)
    boat: dict = field(init=False)

    def __post_init__(self):
        self.init_blinker()
        self.init_glider()
        self.init_boat()
        self.init_beacon()

    def init_blinker(self):
        self.blinker = {(self.x, self.y): 1,
                        (self.x - 1, self.y): 1,
                        (self.x + 1, self.y): 1}

    def init_glider(self):
        self.glider = {(self.x, self.y - 1): 1,
                       (self.x - 1, self.y - 1): 1,
                       (self.x - 1, self.y): 1,
                       (self.x + 1, self.y): 1,
                       (self.x, self.y+ 1): 1}

    def init_boat(self):
        self.boat = {(self.x, self.y - 1): 1,
                     (self.x - 1, self.y - 1): 1,
                     (self.x - 1, self.y ): 1,
                     (self.x + 1, self.y ): 1,
                     (self.x, self.y + 1): 1}

    def init_beacon(self):
        self.beacon = {(self.x  - 1, self.y): 1,
                       (self.x  - 1, self.y - 1): 1,
                       (self.x  - 2, self.y): 1,
                       (self.x  - 2, self.y - 1): 1,
                       (self.x, self.y + 1): 1,
                       (self.x, self.y + 2): 1,
                       (self.x  + 1, self.y + 1): 1,
                       (self.x  + 1, self.y + 2): 1}
