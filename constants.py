# Constants used for various purposes

pixelsPerInch = 144 # pixels per inch
minSize = 0.3 * pixelsPerInch # minimum area a "screw" can be without being ignored
screwHeadTolerance = 0.05 * pixelsPerInch # tolerance for discounting screw head points
peakTolerance = 0.7 # tolerance for discounting noise in peak recognition


# Indentifyable Screw Measurements (for estimating and color indicators)
screwLengths = {
    3/8: (0, 0, 255), # tiny boi -> red
    5/8: (0, 255, 0), # normal boi -> green
    3/4: (255, 0, 0), # funky boi -> blue
    1: (255, 0, 255), # smol wood boi -> purple
    2 + 1/4: (255, 255, 0) # absolute lad - > cyan
}

screwDiameters = {
    3/16: (0, 0, 255), # normal-ish chonk -> red
    1/8: (255, 0, 0) # thin wood -> blue
}

screwThreads = {
    13: (0, 0, 255), # tiny boi -> red
    17: (0, 255, 0), # normal boi AND funky boi -> green
    15: (255, 0, 255), # smol wood boi -> purple
    19: (255, 255, 0) # absolute lad - > cyan
}