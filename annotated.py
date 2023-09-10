# make sure to: pip install opencv-python AND deepface
# opencv is there to interact with the camera and process the frames
# deepface is the neural network behind the program's machine learning

import threading # core python module which allows for simultaneous function calling
import cv2 # opencv
from deepface import DeepFace # this syntax is important to ensure youre importing the right technologies

# now creating a basic opencv camera capture:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # dshow = direct show video input
# cv2 video capture = OS class for processing video frames
# by specifying 0, you're just telling it to pick the first camera in the device
# current device has 1 camera = specify 0
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# specifying the dimensions of the frame captured

# telling the program to only check frames once in a while:
# this is done to avoid overwhelming server
counter = 0 # to track number of frames
face_match = False # global boolean to determine final output
# this boolean will be determined by the "check_face" function
reference_img = cv2.imread("reference.jpg") # you can change this as usage expands --TODO

# the function checking the face
def check_face(frame): # takes the frame (screenshot basically of the recognized face)
    global face_match # telling the function we're using the global one, not creating a new local one with the same name
    try:
        if DeepFace.verify([frame, reference_img.copy()])['verified']: # uses deepface neuralnetwork to verify both faces are the same
            face_match = True # valid face, authorized
        else:
            face_match = False # valid face, not authorized

    except ValueError:
        face_match = False # no valid face, no authorization

# main loop:
while True:
    ret, frame = cap.read() # ret checks if there IS smth (a face)
    # if ret is true it also gets the frame (image) so it can be checked
    if ret:
        # telling it to do smth everytime it is true
        if counter % 30 == 0: # so every 30 frames
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start() # this comma is there to force create a tuple
            except ValueError: # like try&catch statements in java
                # this clause is written because deepface only throws a ValueError when it cant recognize the face
                pass # "pass" is a keyword that allows you to put smth for code to function while telling it to do NTH
        counter += 1 # iterating the counter variable to keep the loop functioning properly
        if face_match: 
            cv2.putText(frame,"MATCH",(20,450), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 3) # instead of using python's pillow!
            # note 1: in cv2 colors are BLUE, GREEN, RED
            # the format here is: .putText(element, text, placement, font, font-size, color, thickness)
        else:
            cv2.putText(frame,"NO MATCH",(20,450), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 3)

        cv2.imshow("video", frame) # will ensure whatever result reached is displayed
    key = cv2.waitKey(1) # this processes user input to accept a key clicked
    if key == ord("q"): # TODO maybe change which is ur esc button?
        break

cv2.destroyAllWindows 
# what does this do: the q acts as our escapebutton.. once its pressed the loop will break and the program will destroy all windows