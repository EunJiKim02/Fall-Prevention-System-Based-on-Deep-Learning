import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import copy

from PIL import Image
from pycaret.classification import *  # type: ignore

from ai.lib.lang_sam.lang_sam import LangSAM
from ai.lib.openpose.src import util
from ai.lib.openpose.src.body import Body


import warnings

warnings.filterwarnings("ignore")

"""
용도: 침대 영역 detection, 키포인트 좌표값 pose estimation, 정상 행동과 낙상 위험 행동 분류 모델 test

"""


def crop_image(image, boxes):
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.axis("off")
    img_x, img_y = image.size

    for box in boxes:
        x_min, y_min, x_max, y_max = box
        box_width = x_max - x_min
        box_height = y_max - y_min

        x_min_crop, y_min_crop, x_max_crop, y_max_crop = box

        # slice image
        x_range = box_width * 0.1
        y_range = box_height * 0.1
        x_min_crop = int(max(0, x_min - x_range))
        x_max_crop = int(min(x_max + x_range, img_x))
        y_min_crop = int(max(0, y_min - y_range))
        y_max_crop = int(min(y_max + y_range, img_y))
        # print(x_min_crop, y_min_crop, x_max_crop, y_max_crop)
        crop_image = image.crop((x_min_crop, y_min_crop, x_max_crop, y_max_crop))

        return crop_image


def bed_detection(model, img_path=None, img=None):
    text_prompt = "bed"

    if img_path is not None:
        image_pil = Image.open(img_path).convert("RGB")
    elif img is not None:
        image_pil = Image.fromarray(img).convert("RGB")
    else:
        raise ValueError("Either img_path or img must be provided")

    masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

    if len(masks) == 0:
        print(f"No objects of the '{text_prompt}' prompt detected in the image.")
        return None
    else:
        cropped_img = crop_image(image_pil, boxes)
        # Convert PIL image to OpenCV image
        open_cv_image = np.array(cropped_img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        return open_cv_image


def get_df_row(height, width, allkeypoints):
    df_rows = []
    for personID, keypoints in allkeypoints.items():
        row = []

        for x, y in keypoints:
            if x != -1:
                x = np.floor((x / width) * 10000) / 10000
            if y != -1:
                y = np.floor((y / height) * 10000) / 10000
            row.append(x)
            row.append(y)

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


def pose_estimation(cropped_img):
    body_estimation = Body("ai/lib/openpose/model/body_pose_model.pth")
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

    keypoints_df = pd.DataFrame(columns=header)
    rows_list = []

    candidate, subset = body_estimation(cropped_img)
    canvas = copy.deepcopy(cropped_img)
    canvas, allkeypoints = util.keypoints_extractor(canvas, candidate, subset)
    height = canvas.shape[0]
    width = canvas.shape[1]

    df_rows = get_df_row(height, width, allkeypoints)

    for row in df_rows:
        row = ["real-time_img"] + list(row)
        row.append(-1)
        rows_list.append(row)

    keypoints_df = pd.concat(
        [keypoints_df, pd.DataFrame(rows_list, columns=header)], ignore_index=True
    )
    result_df = data_refine(keypoints_df)
    return result_df


def fall_detect(pred_df, final_model):
    pred_list = predict_model(final_model, pred_df)["prediction_label"].to_list()
    pred = pred_list[0]

    return pred


# Main class for real-time fall prediction
class realtime_fall_predictor:
    def __init__(self, model_name="best_model"):
        self.lsam = LangSAM("vit_h")
        self.model_path = f"ai/checkpoint/{model_name}"
        self.model = load_model(self.model_path)

    def realtime_predict(self, image, crop=False):
        if crop:
            cropped_img = bed_detection(self.lsam, img=image)
            if cropped_img is None:
                return False
            df = pose_estimation(cropped_img)
        else:
            df = pose_estimation(image)
        if df.empty:
            return False
        pred = fall_detect(df, self.model)
        if pred == 1:
            return True
        return False
