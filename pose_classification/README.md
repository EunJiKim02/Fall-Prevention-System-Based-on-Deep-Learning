
# Pose Classification



- get pretrained openpose model
  ``` bash
  mkdir ./pose_classification/lib/openpose/model
  gdown https://drive.google.com/uc?id=1EULkcH_hhSU28qVc1jSJpCh2hGOrzpjK -O ./pose_classification/lib/openpose/model/body_pose_model.pth
  ```

- detection

  ``` bash
  python pose_classification/bed_detection.py
  ```

- pose estimation

  ``` bash
  python pose_classification/pose_estimation.py
  ```

- classification
  train
  ``` bash
  python pose_classification/fall_detect_train.py
  ```
  
- test
  ``` bash
  python pose_classification/fall_detect_train.py
  ```

