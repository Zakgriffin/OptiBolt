# Functions for displaying retrieved measurements in a human readable way

import cv2
from other import roundRect, imperialFrac
from constants import screwLengths, screwDiameters, screwThreads

lengthKeys = screwLengths.keys()
diameterKeys = screwDiameters.keys()
threadKeys = screwThreads.keys()

pad = 10
frame = None
xB, yB, wB, hB = None, None, None, None

def setFrame(f):
    # Sets the frame for drawing images
    global frame
    frame = f
def setBox(b):
    # Sets coords for box outline
    global xB, yB, wB, hB
    xB, yB, wB, hB = b

def labelMeasure(dimensions, descriptor = '', coord = (0, 0), color = (255, 255, 255)):
    # Labels fractional measurements on frame
    whole, num, den = dimensions
    xf, yf = coord

    cv2.putText(frame, str(whole) + ' in', (xf, yf), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1) # whole
    cv2.putText(frame, str(num), (xf + 20, yf - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1) # numerator
    cv2.putText(frame, str(den), (xf + 20, yf), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1) # denominator
    cv2.putText(frame, descriptor, (xf + 65, yf), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1) # descriptor

    cv2.line(frame, (xf + 20, yf - 12), (xf + 35, yf - 12), color, 1) # fraction bar

def labelMeasureSimple(text, descriptor = '', start = (0, 0), color = (255, 255, 255)):
    # Labels simple measurements on frame
    xf, yf = start
    cv2.putText(frame, str(text), (xf, yf), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
    cv2.putText(frame, descriptor, (xf + 65, yf), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1) # descriptor

def outline():
    # Outlines screw with round rectangle
    roundRect(frame, (xB - pad, yB - pad), (xB + wB + pad, yB + hB + pad), (255, 255, 255), 2, 8, 10)

def labelAllInfo(length, diameter, thread):
    # Labels all information about a screw (length, diameter, thread) on frame
    labelMeasure(imperialFrac(length), 'Length', (xB + wB + 15, yB))
    labelMeasure(imperialFrac(diameter), 'Diam', (xB + wB + 15, yB + 35))
    labelMeasureSimple(thread, 'Threads', (xB + wB + 15, yB + 70), color = (255, 255, 255))

def quickColorInfo(length, diameter, thread):
    # Marks screw with color indicators for easy human sorting
    def getClosest(val, screwList, keysList):
        return screwList.get(val, screwList[min(keysList, key = lambda k: abs(k - val))])
    lengthColor = getClosest(length, screwLengths, lengthKeys)
    diamColor = 0 #getClosest(diameter, screwDiameters, diameterKeys)
    threadColor = 0 #getClosest(thread, screwThreads, threadKeys)

    iSize = 6 # size of an indicator square
    xI = xB + wB + pad
    yI = yB + hB // 2
    cv2.rectangle(frame, (xI - iSize, yI - 3 * iSize), (xI + iSize, yI - iSize), lengthColor, cv2.FILLED)
    cv2.rectangle(frame, (xI - iSize, yI - iSize), (xI + iSize, yI + iSize), diamColor, cv2.FILLED)
    cv2.rectangle(frame, (xI - iSize, yI + iSize), (xI + iSize, yI + 3 * iSize), threadColor, cv2.FILLED)

    cv2.rectangle(frame, (xI - iSize, yI - 3 * iSize), (xI + iSize, yI + 3 * iSize), (255,255,255), 1)