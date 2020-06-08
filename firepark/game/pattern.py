from dataclasses import dataclass, field

@dataclass
class Pattern:
    x: int
    y: int
    pattern: dict = field(init=False)

@dataclass
class Blinker(Pattern):
    def __post_init__(self):
        self.pattern = {(self.x, self.y): 1,
                        (self.x - 1, self.y): 1,
                        (self.x + 1, self.y): 1}

@dataclass
class Glider(Pattern):
    def __post_init__(self):
        self.pattern = {(self.x, self.y - 1): 1,
                        (self.x - 1, self.y - 1): 1,
                        (self.x - 1, self.y): 1,
                        (self.x + 1, self.y): 1,
                        (self.x, self.y+ 1): 1}

@dataclass
class Boat(Pattern):
    def __post_init__(self):
        self.pattern = {(self.x, self.y - 1): 1,
                        (self.x - 1, self.y - 1): 1,
                        (self.x - 1, self.y ): 1,
                        (self.x + 1, self.y ): 1,
                        (self.x, self.y + 1): 1}

@dataclass
class Beacon(Pattern):
    def __post_init__(self):
        self.pattern = {(self.x  - 1, self.y): 1,
                        (self.x  - 1, self.y - 1): 1,
                        (self.x  - 2, self.y): 1,
                        (self.x  - 2, self.y - 1): 1,
                        (self.x, self.y + 1): 1,
                        (self.x, self.y + 2): 1,
                        (self.x  + 1, self.y + 1): 1,
                        (self.x  + 1, self.y + 2): 1}