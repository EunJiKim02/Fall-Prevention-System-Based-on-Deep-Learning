import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np

from openpose.src import model
from openpose.src import util
from openpose.src.body import Body
# from openpose.src.hand import Hand

import os


def main():
    #crop data 불러오기
    body_estimation = Body('openpose/model/body_pose_model.pth')

    mode='train'
    root_path = f'./data/{mode}/crop/'
    folder_list=os.listdir(root_path)
    for folder_name in folder_list:
        risk_or_normal=folder_name
        img_list=os.listdir(os.path.join(root_path,folder_name))
        for img in img_list:
            img_path=os.path.join(root_path, folder_name, img)
            print(img_path)
            oriImg=cv2.imread(img_path)
            candidate, subset = body_estimation(oriImg)
            canvas = copy.deepcopy(oriImg)  
            canvas = util.draw_bodypose(img, canvas, candidate, subset,mode,risk_or_normal)

#crop을 들고와야함. crop이 test_image여야함. 
if __name__ == "__main__":
    main()