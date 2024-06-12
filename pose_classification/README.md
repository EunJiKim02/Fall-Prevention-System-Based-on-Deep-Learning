
# Pose Classification

## requirements
```
pip install -r requirements.txt
```

## How to Use

1. get pretrained openpose model
  ``` bash
  mkdir ./pose_classification/lib/openpose/model
  gdown https://drive.google.com/uc?id=1EULkcH_hhSU28qVc1jSJpCh2hGOrzpjK -O ./pose_classification/lib/openpose/model/body_pose_model.pth
  ```

2. detection

  ``` bash
  python pose_classification/bed_detection.py
  ```

3. pose estimation

  ``` bash
  python pose_classification/pose_estimation.py
  ```

4. classification
- train
  ``` bash
  python pose_classification/fall_detect_train.py
  ```
  
- test
  ``` bash
  python pose_classification/fall_detect_train.py
  ```

