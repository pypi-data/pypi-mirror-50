"""
Bharat Raman
Class for a ball: describes a ball via its mass and radius
"""

class Ball:
    def __init__(self, mass, name = "ball"):
        """
        args: mass(int), name(str)
        """
        self.mass = mass
        self.name = name

    #if user wants to name the ball
    def setName(self, name):
        self.name = name
    def getTerminalVelocity(self):
        return self.mass*9.8/0.47