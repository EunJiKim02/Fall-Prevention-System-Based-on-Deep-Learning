import warnings
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from lang_sam import LangSAM
import os
import cv2
import pandas as pd
warnings.filterwarnings("ignore")
from tqdm import tqdm
'''

https://github.com/luca-medeiros/lang-segment-anything
https://github.com/IDEA-Research/GroundingDINO

용도: 침대 영역 segmentation 및 detection

코드실행 결과
침대 영역을 segmentation 및 detection한 후 이미지를 저장


'''

def save_crop_image(image, boxes, logits, name, mode, risk_or_normal, save_path = None):
    fig, ax = plt.subplots()
    ax.imshow(image)
    # ax.set_title("Image with Bounding Boxes")
    print("==============>",type(image))
    ax.axis('off')
    img_x, img_y = image.size


    for i,(box, logit) in enumerate(zip(boxes, logits)):
        confidence_score = round(logit.item(), 2) 
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
        print(x_min_crop,y_min_crop,x_max_crop,y_max_crop)
        crop_image = image.crop((x_min_crop,y_min_crop,x_max_crop,y_max_crop))

        save_path = f'./data/{mode}/crop/{risk_or_normal}/'
        os.makedirs(save_path, exist_ok=True)
        crop_image = crop_image.resize((512, 512))
        crop_image.save(f"{save_path}{i}_{name}","JPEG")


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height
    
def main():
    model = LangSAM("vit_h")
    text_prompt = "bed"
    mode='train'
    root_path = f'./data/{mode}/origin/'
    #normal, risk folder 이름 저장
    folder_names = os.listdir(root_path)

    for folder_name in folder_names:
        img_list=os.listdir(folder_name)
        risk_or_normal=folder_name
        
        for img_name in tqdm(img_list):
            img_path=os.path.join(root_path, folder_name,img_name)
            # width, height = get_image_size(img_path)
            image_pil = Image.open(img_path).convert("RGB")
            masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

            if len(masks) == 0:
                        print(f"No objects of the '{text_prompt}' prompt detected in the image.")
            else:

                # Display the image with bounding boxes and confidence scores
                save_crop_image(image_pil, boxes, logits, img_name, mode, risk_or_normal)


if __name__ == "__main__":
    main()

