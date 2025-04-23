import pandas as pd
import tensorflow as tf
import numpy as np
import cv2

import subprocess
from io import StringIO

# Model Stuff
characters_label = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
model = tf.keras.models.load_model("isl_model.keras")

# Frame properties
FRAME_NAME = "Press Q to close"
FRAME_HEIGHT = 900
FRAME_WIDTH = 1200

# Region properties
REGION_TOP_LEFT = (272, 272)
REGION_SIZE = (512, 512)
REGION_BOUNDRY_COLOR = (255, 0, 0)
REGION_BOUNDRY_SIZE = 3

# Make capture
capture = cv2.VideoCapture(0)

# Main Loop
frame_number = 0
current_prediction = "Waiting..."
while(True):
    ret, frame = capture.read()
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    frame = cv2.flip(frame, 1)

    region_bottom_right = (REGION_TOP_LEFT[0] + REGION_SIZE[0],
                           REGION_TOP_LEFT[1] + REGION_SIZE[1])
    cv2.putText(frame, current_prediction, (10,20), cv2.FONT_HERSHEY_COMPLEX, 1,( 255, 0, 0),2,cv2.LINE_AA)
    cv2.rectangle(frame, REGION_TOP_LEFT, region_bottom_right,
                  REGION_BOUNDRY_COLOR, REGION_BOUNDRY_SIZE)
    cv2.imshow("Press Q to close", frame)
    frame_number += 1

    if frame_number % 120 == 0:
        # Getting region
        region = frame[REGION_TOP_LEFT[0]:region_bottom_right[0],
                       REGION_TOP_LEFT[1]:region_bottom_right[1]]
        region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        region = cv2.GaussianBlur(region, (5,5), 0)
        region = cv2.resize(region, (128, 128))
        region = cv2.flip(region, 1)
        cv2.imwrite("output.jpg", region)
        
        # Getting prediction
        opt = subprocess.check_output("powershell -command ./sobel.exe " + "output.jpg" + " " + "output.csv")
        inpt = pd.read_csv(StringIO(opt.decode('utf-8')[0:-1]), header=None)
        predictions = model.predict(inpt.values)
        current_prediction = "Prediction is " + characters_label[np.argmax(predictions)]
        
    if (cv2.waitKey(1) == ord('q')):
        break

capture.release()
cv2.destroyAllWindows()
