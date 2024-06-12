import cv2
import os

"""
용도 : 영상을 이미지로 변경

코드실행 결과 : 영상을 각 프레임에 해당하는 이미지로 저장
"""

def save_frames(video_path, output_folder, frame_interval=5):
    cap = cv2.VideoCapture(video_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_count = 0
    saved_frame_count = 0
    
    while True:
       
        ret, frame = cap.read()
        
        if not ret:
            break
        
     
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
        
        frame_count += 1
    
    cap.release()
    print(f"Total saved frames: {saved_frame_count}")


video_path = 'path_to_your_video.mp4' 
output_folder = 'extracted_frames' 
save_frames(video_path, output_folder)
