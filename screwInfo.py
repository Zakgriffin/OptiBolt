# Functions for pulling quantitative values from a cleaned set of points

from constants import pixelsPerInch, peakTolerance

def getLength(tops, bottoms):
    # Returns estimated length of screw
    def length(half):
        return half[len(half) - 1][0] - half[0][0]
    return ((length(tops) + length(bottoms)) / 2) / pixelsPerInch

def getDiameter(tops, bottoms):
    # Returns estimated diameter of screw
    def averageHeight(half):
        average = 0
        for p in half: average += p[1]
        average /= len(half)
        return average
    return (averageHeight(tops) + averageHeight(bottoms)) / pixelsPerInch
def getThreadCount(tops, bottoms):
    # Returns estimated thread count of screw
    def thread(half):
        k = [] # DEBUG - for seeing some important points

        amp = 0 # keeps track of most extreme recent amplitude
        heading = False # boolean that alternates when a peak or valley is reached
        peaks = 0
        for p in half:
            height = p[1] # get y coord of p
            if(heading and (height - peakTolerance > amp)) or (not heading and (height + peakTolerance < amp)):
                # reached either a peak or valley
                if heading: peaks += 1; k.append(p) # peak
                heading = not heading # invert heading boolean, going from peaks, to valleys, or vise versa
            else:
                # not a peak of valley, continue searching
                amp = height
        return peaks, k
    t = thread(tops)
    b = thread(bottoms)
    return (t[0] + b[0]) // 2, t[1] + b[1]
    # return peaks <-- after debug stuffs is removed