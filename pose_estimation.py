import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np

from openpose.src import model
from openpose.src import util
from openpose.src.body import Body
# from openpose.src.hand import Hand

import pandas as pd
import os


def main():

    body_estimation = Body('openpose/model/body_pose_model.pth')
    output = []
    mode='test'
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
            df = util.draw_bodypose(img, canvas, candidate, subset,mode,risk_or_normal)

            if len(output) == 0:
                output = df
            else:
                output = pd.concat([output, df])

        print(output)
    output.to_csv('./data/train/pose/output.csv')

if __name__ == "__main__":
    main()