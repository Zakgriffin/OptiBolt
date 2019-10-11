# Contains function for cleaning contour points for later processing

import math
from constants import screwHeadTolerance

import cv2 #DEBUG - frame and cv2 won't be needed in end product

def cleanPoints(screw, frame):
    # Rotates, flattens, and generally cleans up points for a screw

    # unpack line best fit dy/dx, center at (x, y)
    dx, dy, x, y = screw['line']
    # rotate all points by this angle
    A = math.atan2(dy, dx)

    #cv2.line(frame, (x, y), (20 * math.cos(A) + x, 20 * math.sin(A) + y), (255, 0, 255), 2) # DEBUG
    #cv2.circle(frame, (x, y), 3, (0, 0, 255), -1) # DEBUG

    flatPoints = []
    # rotate all points to have screw laying horizontally, add to flatPoints
    for point in screw['points']:
        # coords relative to center (x, y)
        xOff = x - point[0]
        yOff = y - point[1]

        r = math.sqrt(xOff * xOff + yOff * yOff) # distance
        aOff = math.atan2(yOff, xOff) # angle
        
        # new rotated coords
        xNew = r * math.cos(aOff - A)
        yNew = r * math.sin(aOff - A)

        flatPoints.append([xNew, yNew])

    # split into 2 lists, tops/bottoms
    tops = []
    bottoms = []
    extra = [] # to be appended to beginning of either tops or bottoms

    onTops = flatPoints[0][1] < 0 # whether or not on tops
    crossed = 0 # counts number of times crossed
    for p in flatPoints:
        if (p[1] < 0) != onTops:
            # crossed
            crossed += 1
            onTops = not onTops
        if crossed >= 2:
            extra.append(p)
        elif p[1] < 0:
            tops.append(p)
        else:
            bottoms.append(p)
    # merge extra list with correct half in order
    if onTops: tops = extra + tops
    else: bottoms = extra + bottoms


    # now for the tricky bit...
    for p in tops: p[1] = -p[1] # flip all y for tops
    # find if highest point is to the left or right of center
    highest = (0, 0)
    for p in bottoms:
        if p[1] > highest[1]: highest = p # new best
    if highest[0] < 0:
        for p in tops: p[0] = -p[0]
        for p in bottoms: p[0] = -p[0]
        bottoms = list(reversed(bottoms))
    else:
        tops = list(reversed(tops))
    # now have two lists of cleaned points other than removing head
    def removeHead(half):
        average = 0
        if len(half) == 0:
            return []
        for p in half: average += p[1]
        average /= len(half)

        #cv2.line(frame, (0, average + y), (1000, average + y), (255, 0, 0)) # DEBUG

        for i in range(0, len(half)):
            if half[i][1] > average + screwHeadTolerance:
                half = half[0:i]
                break
        return half
    tops = removeHead(tops)
    bottoms = removeHead(bottoms)

    # DEBUG - very important debug in fact...
    """
    color = 255
    for point in tops:
        color -= 0.8
        cv2.circle(frame, (point[0] + x, point[1] + y), 1, (0, 0, color))
    color = 255
    for point in bottoms:
        color -= 0.8
        cv2.circle(frame, (point[0] + x, point[1] + y), 1, (0, color, 0))
    """
    # DEBUG

    # now have (tops, bottoms) in flat, consistant format and without heads
    return tops, bottoms