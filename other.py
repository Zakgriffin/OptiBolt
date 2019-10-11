# Utility functions

import cv2

def roundRect(frame, topLeft, bottomRight, lineColor, thickness, lineType, cornerRadius):
    # Draws a rect with rounded corners
    """
    corners:
    p1 - p2
    |     |
    p4 - p3
    """
    (tlx, tly) = topLeft
    (brx, bry) = bottomRight


    p1 = [tlx, tly]
    p2 = [brx, tly]
    p3 = [brx, bry]
    p4 = [tlx, bry]

    # draw straight lines
    cv2.line(frame, (p1[0] + cornerRadius,p1[1]), (p2[0] - cornerRadius,p2[1]), lineColor, thickness, lineType)
    cv2.line(frame, (p2[0],p2[1] + cornerRadius), (p3[0],p3[1] - cornerRadius), lineColor, thickness, lineType)
    cv2.line(frame, (p4[0] + cornerRadius,p4[1]), (p3[0] - cornerRadius,p3[1]), lineColor, thickness, lineType)
    cv2.line(frame, (p1[0],p1[1] + cornerRadius), (p4[0],p4[1] - cornerRadius), lineColor, thickness, lineType)

    # draw arcs
    cv2.ellipse(frame, (p1[0] + cornerRadius, p1[1] + cornerRadius), (cornerRadius, cornerRadius), 180, 0, 90, lineColor, thickness, lineType)
    cv2.ellipse(frame, (p2[0] - cornerRadius, p2[1] + cornerRadius), (cornerRadius, cornerRadius), 270, 0, 90, lineColor, thickness, lineType)
    cv2.ellipse(frame, (p3[0] - cornerRadius, p3[1] - cornerRadius), (cornerRadius, cornerRadius), 0.0, 0, 90, lineColor, thickness, lineType)
    cv2.ellipse(frame, (p4[0] + cornerRadius, p4[1] - cornerRadius), (cornerRadius, cornerRadius), 90, 0, 90, lineColor, thickness, lineType)

def imperialFrac(x, largest_denominator=32):
    # Converts decimal into 3 part tuple for fractional imperial measurement
    if x < 0:
        pass
        #raise ValueError("x must be >= 0")
    scaled = int(round(x * largest_denominator))
    whole, leftover = divmod(scaled, largest_denominator)
    if leftover:
        while leftover % 2 == 0:
            leftover >>= 1
            largest_denominator >>= 1
    return whole, leftover, largest_denominator