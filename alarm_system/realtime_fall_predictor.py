import cv2
import time
from ai.predict_for_alarm import realtime_fall_predictor
from backend.database.db import Mysqldb, Patient

def realtime_predictor(source=0, frame_interval=10, id = None):

    user = Patient()
    user.setinfo(id)

    if id is None:
        print("Bed is not selected!")
        return

    cap = cv2.VideoCapture(source)
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
                user.changestatus(True)
            last_time = current_time

        cv2.imshow('Webcam Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    bedid = int(input('현재 찍고 있는 침대 번호를 지정해주세요.'))
    #src = 'http://192.168.0.10:7000/video'
    src = 'test.mp4'
    realtime_predictor(source=src, id = bedid)


main()