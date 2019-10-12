# Contains function for cleaning contour points for later processing

import math
from constants import screwHeadTolerance

import cv2 #DEBUG - frame and cv2 won't be needed in end product

def cleanPoints(screw, frame):
    # Function Outline:
    # 1. Rotate all points of screw by opposite the angle of line of best fit (rotate points to have screw laying horizontally)
    # 2. Assign each point to tops or bottoms lists, splitting screw in half
    # 3. Flip x and y for necessary points so that screw head is on the right
    # 4. Reverse order of necessary lists so that first element is farthest left
    # 5. Find extraneous points to remove head of screw
    # 6. Return tuple of cleaned tops and bottoms

    dx, dy, x, y = screw['line'] # unpack line best fit dy/dx, center at (x, y)
    A = math.atan2(dy, dx) # rotate all points by this angle

    #cv2.line(frame, (x, y), (20 * math.cos(A) + x, 20 * math.sin(A) + y), (255, 0, 255), 2) # DEBUG
    #cv2.circle(frame, (x, y), 3, (0, 0, 255), -1) # DEBUG

    flatPoints = []
    # 1. Rotate all points of screw by opposite the angle of line of best fit
    for point in screw['points']:
        # coords relative to center of screw at (x, y)
        xRel = x - point[0]
        yRel = y - point[1]

        r = math.sqrt(xRel * xRel + yRel * yRel) # distance to point
        aOff = math.atan2(yRel, xRel) # angle to point
        
        # new rotated coords
        xNew = r * math.cos(aOff - A)
        yNew = r * math.sin(aOff - A)

        flatPoints.append([xNew, yNew]) # add to list

    # 2. Assign each point to tops or bottoms lists, splitting screw in half
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

    # find if highest point is to the left or right of center
    highest = (0, 0) # coord of heighest point (on head of screw)
    for p in bottoms:
        if p[1] > highest[1]: highest = p # found new highest

    # 3. Flip x and y for necessary points so that screw head is on the right

    # y coords
    for p in tops: p[1] = -p[1] # always have to negate y coord of all in tops
    # never have to negate y coord of all in bottoms

    # x coords
    if highest[0] < 0:
        # screw head was on left
        for p in tops: p[0] = -p[0] # negate x coord of all in tops
        for p in bottoms: p[0] = -p[0] # negate x coord of all in bottoms
        
    # 4. Reverse order of necessary lists so that first element is farthest left
        bottoms = list(reversed(bottoms)) # reverse list of bottoms
    else:
        # screw head is on right
        tops = list(reversed(tops)) # reverse list of tops

    # 5. Find extraneous points to remove head of screw
    def removeHead(half):
        # sub function applied to tops and bottoms
        average = 0
        if len(half) == 0:
            return []
        for p in half: average += p[1]
        average /= len(half) # average is now roughly radius of screw

        #cv2.line(frame, (0, average + y), (1000, average + y), (255, 0, 0)) # DEBUG

        for i in range(0, len(half)):
            if half[i][1] > average + screwHeadTolerance:
                # found start of screw head, discard rest of list
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

    if len(tops) == 0 or len(bottoms) == 0:
        # no points left on screw after cleaning, invalid screw
        return None, None, True

    # 6. Return tuple of cleaned tops and bottoms
    return tops, bottoms, False