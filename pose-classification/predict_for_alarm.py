import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import copy

from PIL import Image
from lib.lang_sam import LangSAM
from lib.openpose.src import util
from lib.openpose.src.body import Body
from pycaret.classification import *  # type: ignore

import warnings

warnings.filterwarnings("ignore")


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


def bed_detection(model, img_path):

    cropped_img = None
    text_prompt = "bed"
    image_pil = Image.open(img_path).convert("RGB")
    masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

    if len(masks) == 0:
        print(f"No objects of the '{text_prompt}' prompt detected in the image.")
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
    body_estimation = Body("openpose/model/body_pose_model.pth")
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

    candidate, subset = body_estimation(cropped_img)
    canvas = copy.deepcopy(cropped_img)
    canvas, allkeypoints = util.keypoints_extractor(canvas, candidate, subset)
    height = canvas.shape[0]
    width = canvas.shape[1]
    df_rows = get_df_row(height, width, allkeypoints)
    # print(df_rows)
    for row in df_rows:
        # kepoints_df.append(row)
        kepoints_df.loc[df_index] = row
        df_index += 1

    result_df = data_refine(kepoints_df)

    return result_df


def fall_detect(pred_df, final_model):
    pred_list = predict_model(final_model, pred_df)["prediction_label"].to_list()
    pred = pred_list[0]

    return pred


def main():
    lsam = LangSAM("vit_h")
    test_dir = f"data/test/"
    img_pathes = [test_dir + img for img in os.listdir(test_dir)]
    model_name = ""
    model_name = model_name.split(".")[0]
    model_path = f"checkpoint/{model_name}"
    model = load_model(model_path)

    for test_img in img_pathes:
        cropped_img = bed_detection(lsam, test_img)
        df = pose_estimation(cropped_img)
        pred = fall_detect(df, model)
        if pred == 1:
            print("Fall detected")
            # send_alarm()


if __name__ == "__main__":
    main()