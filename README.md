# Fall Prevention System based on Deep Learning

2024-1학기 종합설계프로젝트2


### Project 소개
딥러닝 기반의 낙상사고 방지 시스템



![image](https://github.com/EunJiKim02/Fall-Prevention-System-Based-on-Deep-Learning/assets/100736860/09b5eef4-e92e-42f8-a92d-6046cab02f93)


### dataset

https://drive.google.com/drive/folders/1NCKVH2z7ljYXVJDb2eQDjhm2fmP9RDzY?usp=share_link


### environment setting

- conda environment

  ``` bash
  conda env create -f environment.yaml
  conda activate fall
  ```

- get pretrained openpose model
  ``` bash
  mkdir ./openpose/model

  gdown https://drive.google.com/uc?id=1EULkcH_hhSU28qVc1jSJpCh2hGOrzpjK -O ./openpose/model/body_pose_model.pth
  ```

- detection

  ``` bash
  python bed_seg_detection.py
  ```

- pose estimation

  ``` bash
  python pose_estimation.py
  ```

- classification
  train
  ``` bash
  python fall_detect_train.py
  ```
  test
  ``` bash
  python fall_detect_train.py
  ```




### Member


|김은지|김찬호|문채원|하재현|
| :---------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------: |
|   ![image](https://avatars.githubusercontent.com/u/87495422?v=4) |  ![image](https://avatars.githubusercontent.com/u/105068708?v=4) |  ![image](https://avatars.githubusercontent.com/u/111948424?v=4)  |  ![image](https://avatars.githubusercontent.com/u/100736860?v=4)  |
| <a href="https://github.com/EunJiKim02" target="_blank"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a> | <a href="https://github.com/coolho1129" target="_blank"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a> | <a href="https://github.com/mchaewon" target="_blank"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a> | <a href="https://github.com/jaehyeonha" target="_blank"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
|컴퓨터학부|컴퓨터학부|컴퓨터학부|컴퓨터학부 <br> 글로벌소프트웨어융합|
| 2021111183 | 2021114818 | 2021114611 | 2021115737 |

<br> </br>
