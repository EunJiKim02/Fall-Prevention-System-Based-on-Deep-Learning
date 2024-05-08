import warnings
import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
from tqdm import tqdm

from openpose.src import model
from openpose.src import util2
from openpose.src.body import Body
# from openpose.src.hand import Hand

import pandas as pd
import os

warnings.filterwarnings("ignore")

def generate_dataframe(height, width, allkeypoints, mode, classname, filename):
    # i : 관절번호
    # n : 사람 번호 (여러 명 있을 때)
    # x , y

    
    name = mode+"_"+classname +"_"+ filename
    df_rows = []
    for personID, keypoints in allkeypoints.items():
        #pointer = 0
        row = []
        row.append(name)
        # for i in range(18):

        #     if pointer >= len(group_entries) or (i != group_entries[pointer][0]):
        #         temp.append(-1)
        #         temp.append(-1)
        #     else:
        #         X = np.floor((group_entries[pointer][1] / width) * 10000) / 10000
        #         Y = np.floor((group_entries[pointer][2] / height) * 10000) / 10000
        #         temp.append(X)
        #         temp.append(Y)
        #         pointer += 1

        for x,y in keypoints:
            if x!=-1:
                x = np.floor((x / width) * 10000) / 10000  
            if y!=-1:
                y = np.floor((y / width) * 10000) / 10000\
                
            row.append(x)
            row.append(y)
        
        
        if classname == 'risk':
            row.append(1)
        else:
            row.append(0)

        df_rows.append(row)
        # writer.append(temp)

    return df_rows

def main():

    body_estimation = Body('openpose/model/body_pose_model.pth')
    mode='test'
    root_path = f'./data/{mode}/crop/'
    folder_list=os.listdir(root_path)
    header = ['Img', 'NoseX', 'NoseY', 'NeckX','NeckY', 'RShoulderX','RShoulderY','RElbowX','RElbowY', 'RWristX','RWristY', 'LShoulderX','LShoulderY', 
                         'LElbowX','LElbowY', 'LWristX','LWristY', 'MidHipX','MidHipY', 'RHipX','RHipY', 'RKneeX','RKneeY','AnkleX','AnkleY', 'LHipX','LHipY', 
                         'LAnkleX','LAnkleY', 'REyeX', 'REyeY','LEyeX', 'LEyeY','REarX','REarY', 'LEarX','LEarY', 'label']
    kepoints_df = pd.DataFrame(columns=header)
    df_index = 0 
    for folder_name in folder_list:
        classname=folder_name
        img_list=os.listdir(os.path.join(root_path,folder_name))
        for img in tqdm(img_list):
            img_path=os.path.join(root_path, folder_name, img)
            #print(img_path)
            oriImg=cv2.imread(img_path)
            candidate, subset = body_estimation(oriImg)
            canvas = copy.deepcopy(oriImg)  
            canvas, allkeypoints = util2.keypoints_extractor(canvas, candidate, subset)
            height = canvas.shape[0]
            width = canvas.shape[1]
            df_rows = generate_dataframe(height, width, allkeypoints, mode, classname, img)
            #print(df_rows)
            for row in df_rows:
                #kepoints_df.append(row)
                kepoints_df.loc[df_index] = row
                df_index+=1
        #print(output)
    kepoints_df.to_csv(f'./data/{mode}/pose/output.csv', index = False)

if __name__ == "__main__":
    main()