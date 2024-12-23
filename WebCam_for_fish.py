import cv2
import time
import numpy as np
from tflite_runtime.interpreter import Interpreter
from threading import Thread
import os  # Added to handle file paths
import requests

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, resolution=(640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True

min_conf_threshold = 0.5  # Minimum confidence threshold for displaying detected objects default 0.5

# Path to .tflite file, which contains the model that is used for object detection
tflite_model_path = "/home/user/Downloads/mobilenet_ssd_v2_coco_quant_postprocess.tflite"
# Path to label map file
Labels_path = "/home/user/Downloads/coco_labels.txt"  # from MobileNet SSD v2 (COCO)

indexs = []
labels = []
# Load the label map
with open(Labels_path, 'r') as f:
    labels_data = [line.strip() for line in f.readlines()]
    for count in range(0, len(labels_data)):
        indexs.append(labels_data[count].split("  ")[0])
        labels.append(labels_data[count].split("  ")[1])

# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = input_details[0]['dtype'] == np.float32

input_mean = 127.5
input_std = 127.5

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

imW = 640
imH = 480

# Initialize video stream
videostream = VideoStream(resolution=(imW, imH), framerate=30).start()
time.sleep(1)

# Define the path to save the image on the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
image_path = os.path.join(desktop_path, "detected_object.jpg")


url = "https://notify-api.line.me/api/notify"
token = "H71DKEntyeYy8vTFxuZByY0gcPiiZKkeiTl04Qks9Mq"
headers = {'Authorization': 'Bearer ' + token}

# Define the list of objects to detect
objects_to_detect = ['person', 'bird', 'dog', 'cat', 'zebra']

while True:
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Grab frame from video stream
    frame1 = videostream.read()

    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e., if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence of detected objects

    # Initialize a flag to check if any desired object is detected
    object_detected = False
    
    cnt=0
    k=1
    temp = ''

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if (scores[i] > min_conf_threshold) and (scores[i] <= 1.0):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions,
            # need to force them to be within image using max() and min()
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            # Draw label
            object_name = labels[int(classes[i])]  # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
            label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
            cv2.rectangle(
                frame,
                (xmin, label_ymin - labelSize[1] - 10),
                (xmin + labelSize[0], label_ymin + baseLine - 10),
                (255, 255, 255),
                cv2.FILLED,
            )  # Draw white box to put label text in
            cv2.putText(
                frame,
                label,
                (xmin, label_ymin - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                2,
            )  # Draw label text

            # Check if the detected object is in the list of desired objects
            if object_name in objects_to_detect:
                print(object_name)
                temp =temp + object_name
                object_detected = True  # Set the flag to True

    # Save frame to desktop if any desired object is detected
    if object_detected and k:
        print(k)
        time.sleep(1)
        cv2.imwrite(image_path, frame)  # Save the frame with bounding boxes and labels
        object_detected = False
        
        st = 'Alert ' + str(object_name) + ' detected'
        temp = ''
        msg = {
        'message': (None, st),
        'imageFile': open("/home/user/Desktop/detected_object.jpg","r+b" ),
        #'imageFullsize': open("/home/user/Desktop/dead_fish_two.jpeg"),
        }

        res = requests.post(url, headers=headers, files=msg)
        k=0
        
    if k==0:
        cnt=cnt+1
        
    if cnt>=1e9:
        k=1
    

    # Draw framerate in corner of frame
    cv2.putText(
        frame,
        'FPS: {0:.2f}'.format(frame_rate_calc),
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2,
        cv2.LINE_AA,
    )

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
videostream.stop()



