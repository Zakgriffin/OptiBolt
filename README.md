# OptiBolt
A Python and Opencv based tool for optical screw recognition including features for fast human sorting speeds

Interested in trying out OptiBolt?

What you will need:
1. A PC or Mac capable of running python scripts
2. A mobile phone to act as a webcam (or just a powerful camera, if you have this, skip steps 3 through 7)
3. A light table to place screws onto. I've been using "Logan: Light Box" from god knows how many years ago. See https://www.bhphotovideo.com/c/product/32011-REG/Logan_Electric_750428_8_x_10_Desk.html

Steps:
1. Download Python (3.7 recommended) from https://www.python.org/downloads/
2. Install opencv by running `pip install opencv-python` after python installation
3. Download the EpocCam drivers to use your mobile device as a webcam from http://www.kinoni.com/
4. Download the EpocCam Viewer application from http://www.kinoni.com/
5. Download the EpocCam app on your mobile device
  IMPORTANT: I recommend the EpocCam HD app for $7.99 for higher quality video
6. Open EpocCam Viewer on your PC or Mac, as well as the Epoccam App on your mobile device
7. Make sure there is a connection between your mobile device and viewer by opening some camera application on your PC or Mac. Video should be streaming
8. Position your mobile phone close to 3.5 inches above your light table facing down. Make sure it is stable and flat
9. Run the `optiBolt.py` script from either a command line, or within an integrated editor like Visual Studio Code (follow this for the latter: https://code.visualstudio.com/docs/languages/python)
10. Throw some screws under the thing. As of now, it probably won't work at all, but changes are to be made and hopefully will make this fully functional.

Also:
You may need to play with the slider that appears on the main window to tinker with threshhold values for creating the mask. Complicated words, just move it around until it kinda works.
