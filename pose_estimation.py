import warnings
import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
from tqdm import tqdm

from openpose.src import model
from openpose.src import util
from openpose.src.body import Body

# from openpose.src.hand import Hand

import pandas as pd
import os

warnings.filterwarnings("ignore")


def get_df_row(height, width, allkeypoints, mode, classname, filename):
    name = mode + "_" + classname + "_" + filename
    df_rows = []
    for personID, keypoints in allkeypoints.items():
        row = []
        row.append(name)

        for x, y in keypoints:
            if x != -1:
                x = np.floor((x / width) * 10000) / 10000
            if y != -1:
                y = np.floor((y / height) * 10000) / 10000
            row.append(x)
            row.append(y)

        if classname == "risk":
            row.append(1)
        else:
            row.append(0)

        df_rows.append(row)

    return df_rows


def data_refine(df):
    # 각 행의 -1의 개수를 세어 새로운 열을 만듭니다.
    df["minus_ones_count"] = df.apply(lambda row: (row == -1).sum(), axis=1)

    # -1의 개수가 적은 순으로 정렬하고 이미지 이름이 중복된 행을 제거합니다.
    df_result = df.sort_values(by="minus_ones_count").drop_duplicates(
        subset="Img", keep="first"
    )

    # 이미지 이름을 기준으로 정렬하고 -1의 개수 열을 제거합니다.
    df_result.drop(columns=["minus_ones_count"], inplace=True)
    df_result = df_result.sort_values(by="Img")

    # 불필요한 열을 제거합니다.
    df_result = df_result.drop(
        [
            "NoseX",
            "NoseY",
            "REyeX",
            "REyeY",
            "LEyeX",
            "LEyeY",
            "REarX",
            "REarY",
            "LEarX",
            "LEarY",
        ],
        axis=1,
    )

    return df_result


def main():

    body_estimation = Body("openpose/model/body_pose_model.pth")
    mode = "test"
    root_path = f"./data/{mode}/crop/"
    folder_list = os.listdir(root_path)
    header = [
        "Img",
        "NoseX",
        "NoseY",
        "NeckX",
        "NeckY",
        "RShoulderX",
        "RShoulderY",
        "RElbowX",
        "RElbowY",
        "RWristX",
        "RWristY",
        "LShoulderX",
        "LShoulderY",
        "LElbowX",
        "LElbowY",
        "LWristX",
        "LWristY",
        "MidHipX",
        "MidHipY",
        "RHipX",
        "RHipY",
        "RKneeX",
        "RKneeY",
        "AnkleX",
        "AnkleY",
        "LHipX",
        "LHipY",
        "LAnkleX",
        "LAnkleY",
        "REyeX",
        "REyeY",
        "LEyeX",
        "LEyeY",
        "REarX",
        "REarY",
        "LEarX",
        "LEarY",
        "label",
    ]
    kepoints_df = pd.DataFrame(columns=header)
    df_index = 0

    for folder_name in folder_list:
        classname = folder_name
        img_list = os.listdir(os.path.join(root_path, folder_name))
        for img in tqdm(img_list):
            img_path = os.path.join(root_path, folder_name, img)
            # print(img_path)
            oriImg = cv2.imread(img_path)
            candidate, subset = body_estimation(oriImg)
            canvas = copy.deepcopy(oriImg)
            canvas, allkeypoints = util2.keypoints_extractor(canvas, candidate, subset)
            height = canvas.shape[0]
            width = canvas.shape[1]
            df_rows = get_df_row(height, width, allkeypoints, mode, classname, img)
            # print(df_rows)
            for row in df_rows:
                kepoints_df.loc[df_index] = row
                df_index += 1

    result_df = data_refine(kepoints_df)
    result_df.to_csv(f"./data/{mode}/pose/dataset.csv", index=False)


if __name__ == "__main__":
    main()
