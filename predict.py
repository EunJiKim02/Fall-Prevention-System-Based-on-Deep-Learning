import warnings
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from lang_sam import LangSAM
import numpy as np
import os
import cv2
import pandas as pd
from openpose.src import util
from openpose.src.body import Body
import copy
from sklearn.metrics import accuracy_score
from pycaret.classification import *

warnings.filterwarnings("ignore")
from tqdm import tqdm


def crop_image(image, boxes):
    fig, ax = plt.subplots()
    ax.imshow(image)
    # ax.set_title("Image with Bounding Boxes")
    print("==============>", type(image))
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
        print(x_min_crop, y_min_crop, x_max_crop, y_max_crop)
        crop_image = image.crop((x_min_crop, y_min_crop, x_max_crop, y_max_crop))

        return crop_image


def data_preprocessing(img_path):
    model = LangSAM("vit_h")
    text_prompt = "bed"
    cropped_img = None
    # width, height = get_image_size(img_path)
    image_pil = Image.open(img_path).convert("RGB")
    masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

    if len(masks) == 0:
        print(f"No objects of the '{text_prompt}' prompt detected in the image.")
    else:
        cropped_img = crop_image(image_pil, boxes)
    print(type(cropped_img))  
    open_cv_image = np.array(cropped_img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  

    return open_cv_image


def pose_estimation(cropped_img):
    body_estimation = Body("openpose/model/body_pose_model.pth")

    mode = "test"
    risk_or_normal = "test"
    # oriImg = cv2.imread(img_path)
    candidate, subset = body_estimation(cropped_img)
    #print(type(cropped_img))
    canvas = copy.deepcopy(cropped_img)
    df = util.draw_bodypose(
        mode, canvas, candidate, subset, mode, risk_or_normal
    )

    return df

def fall_detect_predict(csv_file, gt_csvfile, model_path, save_path):
    pred_df = pd.read_csv(csv_file)
    gt_df = pd.read_csv(gt_csvfile)

    final_model = load_model(model_path)
    pred_list = predict_model(final_model, pred_df)["prediction_label"].to_list()
    pred_df["pred"] = pred_list
    gtlist = gt_df["gt"].tolist()

    save_csv_path = os.path.join(save_path, "result.csv")
    pred_df.to_csv(save_csv_path)
    print("Complete save result.csv")

    # accuracy 계산
    acc = accuracy_score(gtlist, pred_list)
    acc *= 100

    print(f"F1 Score : {acc :.2f}")


def main():
    img_path = ['data/test/0_1.jpg', 'data/test/0_1 copy.jpg']
    for d in img_path:
        cropped_img = data_preprocessing(d)
        df = pose_estimation(cropped_img)
        print(df)


if __name__ == "__main__":
    main()