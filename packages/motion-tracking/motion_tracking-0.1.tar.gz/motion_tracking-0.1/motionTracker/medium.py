"""
Bharat Raman
Simple class to describe the fluid the ball is traversing through.
For the scope of this project, the only characteristic of the fluid we need is its density

Not used for now, but can be developed for when quadratic drag is implemented
"""
class Medium:
    def __init__(self,density):
        self.density = density
    