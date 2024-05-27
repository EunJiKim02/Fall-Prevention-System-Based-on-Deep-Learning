import cv2
import time
from pose_classification.predict_for_alarm import realtime_fall_predictor

#cap = cv2.VideoCapture('test.mp4')
cap = cv2.VideoCapture('http://192.168.0.10:7000/video')

frame_interval = 1 / 15.0

last_time = time.time()

fp = realtime_fall_predictor()

print("real-time predictor start")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    current_time = time.time()
    if current_time - last_time >= frame_interval:
        is_fall_detected = fp.realtime_predict(frame)
        if is_fall_detected:
            print("Fall detected!")
        last_time = current_time

    cv2.imshow('Webcam Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()