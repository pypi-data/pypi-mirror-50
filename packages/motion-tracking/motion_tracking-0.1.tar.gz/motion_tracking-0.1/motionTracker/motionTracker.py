"""
Bharat Raman: Ball motion tracker
Track the motion of a ball using kinematic equations in 3D space
"""
from .ball import Ball
from .medium import Medium
import math
#CODE HERE: ID the backend to make pyplot work
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

class motionTracker:
    def __init__(self, mass, speed, horAngle, verAngle, accuracy):
        
        #below is the ball's velocity's x, y, and z coordinate
        self.v = [0,0,0]
        #below three are trackers for the ball's x, y, and z positions. They will be used to plot the motion of the ball
        self.xArray = []
        self.yArray = []
        self.zArray = []
        self.hArray = []
        self.tArray = []
        #Instantiating the ball
        self.thisBall = Ball(mass)
        #setting self.v by interpreting below arguments in terms of spherical coordinates
        self.setInitialVelocity(speed, horAngle, verAngle)
        #below is used to set the accuracy for which the motion is tracked.
        #time is default to 1 second per calculation. To increase accuracy, divide t by accuracy
        self.accuracy = accuracy
        
        #Have the user name the ball
        self.userInput()
        #Store the path of the ball in the arrays
        self.getPath()
        #plot the path using the filled arrays
        self.plotPath()
    
    def userInput(self):
        #STEP 1: Ball setup (its name and its mass)
        print("Name your ball, or hit enter to keep default 'ball'")
        ballName = input()
        if (len(ballName) > 0):
            self.thisBall.name = ballName
        
            
    def setInitialVelocity(self, speed, horAngle, verAngle):
        #setting the initial velocity of the ball. Using the angles, can set up self.v
        #horizontal angle must be between 0 and 360 degrees
        #vertical angle must be between 0 and 90 degrees
        #speed must be greater than 0
        assert(horAngle >= 0 and horAngle <= 360)
        assert(verAngle >= 0 and verAngle <= 90)
        assert(speed > 0)
        #Horizontal and vertical angles in radians
        rH = 2*math.pi*horAngle/360
        rV = 2*math.pi*verAngle/360
        
        #Set the x, y, and z coord of the ball's velocity respectively
        self.v[0] = speed * math.cos(rV)*math.cos(rH)
        self.v[1] = speed * math.cos(rV)*math.sin(rH)
        self.v[2] = speed * math.sin(rV)
        
    def getCoord(self,t):
        m = self.thisBall.mass
        v_t = self.thisBall.getTerminalVelocity()
        #Equations for x, y and z coordinates of a ball in motion with air resistnace
        thisX = (self.v[0]/9.8) * v_t*(1-math.exp(-9.8*t/v_t))
        thisY = (self.v[1]/9.8) * v_t*(1-math.exp(-9.8*t/v_t))
        thisZ = (v_t/9.8)*(self.v[2]+v_t)*(1-math.exp(-9.8*t/v_t)) - v_t*t
        if thisZ < 0:
            thisZ = 0
        
        return [thisX,thisY,thisZ]
    
    def getPath(self):
        #Below arrays will be plotted to show a visual representation of the ball's motion in the air
        while True:
            t = len(self.zArray)/self.accuracy
            coord = self.getCoord(t)
            self.xArray.append(coord[0])
            self.yArray.append(coord[1])
            self.hArray.append(math.sqrt(coord[0]**2 + coord[1]**2))
            self.zArray.append(coord[2])
            self.tArray.append(t)
            if self.zArray[-1] == 0 and len(self.zArray) > 5:
                break
    def plotPath(self):
        #First, visual representation of the ball's horizontal path
        plt.figure(1)
        plt.plot(self.xArray,self.yArray,'r.-')
        plt.xlim(-1*max(self.hArray),max(self.hArray))
        plt.ylim (-1*max(self.hArray),max(self.hArray))
        plt.xlabel('x(t)')
        plt.ylabel('y(t)')
        plt.title("Path of " + self.thisBall.name + " on x-y plane (m)")
        
        #Next, visual representation of the ball's height over time
        plt.figure(2)
        plt.plot(self.hArray, self.zArray, 'b.-')
        plt.xlim(0,1.5*self.hArray[-1])
        plt.ylim(0,1.5*max(self.zArray))
        plt.xlabel('sqrt(x(t)^2 + y(t)^2)')
        plt.ylabel('z(t)')
        plt.title("Height of " + self.thisBall.name +
                  " in relation to horizontal path (m)")
        plt.show()