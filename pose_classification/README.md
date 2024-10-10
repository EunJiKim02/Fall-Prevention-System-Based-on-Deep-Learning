
# Pose Classification

## requirements
```
pip install -r requirements.txt
```

## How to Use

1. get pretrained openpose model
  ``` bash
  mkdir ./lib/openpose/model
  gdown https://drive.google.com/uc?id=1EULkcH_hhSU28qVc1jSJpCh2hGOrzpjK -O 
  ./lib/openpose/model/body_pose_model.pth
  ```

2. detection

  ``` bash
  python bed_detection.py
  ```

3. pose estimation

  ``` bash
  python pose_estimation.py
  ```

4. classification
- train
  ``` bash
  python fall_detect_train.py
  ```
  
- test
  ``` bash
  python fall_detect_train.py
  ```

