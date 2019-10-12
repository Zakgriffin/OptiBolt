# Main file handling image capture and overall procedure

import cv2
import display as dp

from screwInfo import getThreadCount, getLength, getDiameter
from constants import pixelsPerInch, minSize
from cleaner import cleanPoints

cv2.namedWindow("Frame")
cap = cv2.VideoCapture(0) # video capture
cv2.createTrackbar("thresh", "Frame", 80, 255, lambda _: None) # trackbar for threshhold


while(True):
    # main continuous loop
    if cv2.waitKey(1) & 0xFF == ord('q'): break # exit when "q" pressed

    thresh = cv2.getTrackbarPos("thresh", "Frame") # get trackbar threshold value
    """
    # DEBUG - for static image
    frame = cv2.imread('./example.png')
    height, width, _ = frame.shape # get size of window
    s = 2

    frame = cv2.resize(frame, (width * s, height * s))
    # DEBUG - for static image
    """
    _, frame = cap.read() # capture frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # to grayscale
    _, mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY_INV) # to binary mask

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # grab contours

    screws = [] # create list of screws found in frame
    # convert necessary data from contours into screw dicts
    for ctr in contours:
        box = cv2.boundingRect(ctr) # bounding box of screw
        _, _, wB, hB = box
        if wB * hB < minSize: continue # too small to be valid screw

        # restructure points into list of length 2 lists (points)
        points = []
        for i in range(0, len(ctr)): points.append(ctr[i][0])

        screws.append({
            'points': points,
            'box': box,
            'line': cv2.fitLine(ctr, cv2.DIST_WELSCH, 100, 0, 0)
        })

    dp.setFrame(frame) # set frame for use in display
    for screw in screws:
        # clean up points: rotate to flat, remove head, split into top and bottom lists
        tops, bottoms, invalid = cleanPoints(screw, frame)

        if invalid: continue # invalid screw after cleaning

        # grab screw info
        length = getLength(tops, bottoms)
        diameter = getDiameter(tops, bottoms)
        threadCount, points = getThreadCount(tops, bottoms)

        dp.setBox(screw['box']) # set box dimensions for use in display

        dp.outline() # outline the screw with rounded box
        allInfo = True
        if allInfo:
            # label all measurment info for screw
            dp.labelAllInfo(length, diameter, threadCount)
        else:
            # use color indicators for easy human sorting
            dp.quickColorInfo(length, diameter, threadCount)

        # DEBUG
        #for p in points:
        #    cv2.circle(frame, (int(p[0] * 2) + 375, int(p[1] * 2) + 246), 3, (0, 0, 255), -1)
        # DEBUG

    # display final image
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

# when exited, release the capture
cap.release()
cv2.destroyAllWindows()