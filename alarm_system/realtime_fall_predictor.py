import cv2
import time
import concurrent.futures
from ai.predict_for_alarm import realtime_fall_predictor
from backend.database.db import Mysqldb, Patient

def realtime_predictor(source=0, frame_interval=5, id=None, max_width=128, max_height=128):

    user = Patient()
    user.setinfo(id)

    if id is None:
        print("Bed is not selected!")
        return

    cap = cv2.VideoCapture(source)

    original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    aspect_ratio = original_width / original_height
    if max_width / aspect_ratio <= max_height:
        width = max_width
        height = int(max_width / aspect_ratio)
    else:
        width = int(max_height * aspect_ratio)
        height = max_height

    # 줄인 해상도로 설정
    print(width, height)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    fp = realtime_fall_predictor()
    last_time = time.time()

    print("real-time predictor start")

    def predict_with_timeout(frame):
        try:
            result = fp.realtime_predict(frame)
            return result
        except Exception as e:
            print(f"Prediction error: {e}")
            return False

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = None
        while True:
            current_time = time.time()
            ret, frame = cap.read()
            cv2.imshow('Webcam Stream', frame)
            if current_time - last_time >= frame_interval:
                if not ret:
                    print("Failed to grab frame")
                    break

                if future is None:
                    future = executor.submit(predict_with_timeout, frame)
                    last_time = current_time
                elif future.done():
                    if future.exception():
                        print(f"Exception in future: {future.exception()}")
                    if future.result():
                        print("Fall detected!")
                        user.changestatus(True)
                    future = executor.submit(predict_with_timeout, frame)
                    last_time = current_time
        

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.05) 

    cap.release()
    cv2.destroyAllWindows()

def main():
    bedid = int(input('현재 찍고 있는 침대 번호를 지정해주세요 : '))
    # src = 'http://192.168.0.10:7000/video'
    src = 'test2.mp4'
    realtime_predictor(source=src, id=bedid)

main()
