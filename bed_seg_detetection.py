import warnings
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from lang_sam import LangSAM
import os
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

def save_image_with_boxes(image, boxes, logits,name,mode,save_path = None):
    fig, ax = plt.subplots()
    ax.imshow(image)
    # ax.set_title("Image with Bounding Boxes")
    ax.axis('off')

    for i,(box, logit) in enumerate(zip(boxes, logits)):
        confidence_score = round(logit.item(), 2) 
        x_min, y_min, x_max, y_max = box
        box_width = x_max - x_min
        box_height = y_max - y_min

        # Draw bounding box
        rect = plt.Rectangle((x_min, y_min), box_width, box_height, fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

        # Add confidence score as text
        ax.text(x_min, y_min, f"wheels{i+1}", fontsize=8, color='red', verticalalignment='top')
        ax.text(x_max, y_max, f"{confidence_score}", fontsize=8, color='red',verticalalignment='bottom')
    
    if not save_path:
        save_path = f'./data/img/lsam_output/{mode}/box/'
    os.makedirs(save_path, exist_ok=True)
    save_path = save_path + f'{name}_box.png'
    plt.savefig(save_path, bbox_inches='tight')
    plt.show(block=True)


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        return width, height
    
# segmetation code
def overlay_mask_on_image(image, masks, detect_path):
    overlaid_image = np.array(image)

    for  mask_np in masks:
        # 확장된 마스크를 RGB 이미지 크기에 맞게 조절
        expanded_mask = np.expand_dims(mask_np, axis=2)
        expanded_mask = np.repeat(expanded_mask, 3, axis=2)

        # 이미지에 마스크를 덧씌우기
        overlaid_image = np.where(expanded_mask > 0, [255, 255, 0], overlaid_image)  # 노란색 마스크를 사용 (R=255, G=255, B=0)

    overlaid_image = Image.fromarray(overlaid_image.astype(np.uint8))
    overlaid_image.save(detect_path)

def save_masked_image(image, masks, detect_path):
    num_masks = len(masks)

    fig, axes = plt.subplots(1, num_masks + 1, figsize=(15, 5))
    axes[0].imshow(image)
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    for i, mask_np in enumerate(masks):
        axes[i+1].imshow(mask_np, cmap='gray')
        axes[i+1].set_title(f"Mask {i+1}")
        axes[i+1].axis('off')

    plt.tight_layout()
    plt.savefig(detect_path, bbox_inches='tight')
    plt.close()
    print('masked image saved')

def save_mask(mask_np, filename):
    mask_image = Image.fromarray((mask_np * 255).astype(np.uint8))
    mask_image.save(filename)
    
def main():
    model = LangSAM("vit_h")
    text_prompt = "bed"
    mode = 'train'
  
    path = f'./data/img/source/{mode}/'
    names = os.listdir(path)
  
    for name in tqdm(names):
        img_path = path + name
        width, height = get_image_size(img_path)
        image_pil = Image.open(img_path).convert("RGB")
        masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

        if len(masks) == 0:
                    print(f"No objects of the '{text_prompt}' prompt detected in the image.")
        else:
            # Convert masks to numpy arrays
            masks_nps = [mask.squeeze().cpu().numpy().astype('uint8') for mask in masks]

            # Display the image with bounding boxes and confidence scores
            save_image_with_boxes(image_pil, boxes, logits,name)
            detect_mask_path = f'./data/lsam/{mode}/mask/'
            os.makedirs(detect_mask_path,exist_ok=True)
            detect_mask_path = detect_mask_path+f'mask{name}'
            overlay_mask_on_image(image_pil, masks, detect_mask_path)
            
            # Save the masks
            mask_path = f"./data/lsam/{mode}/image_mask/{name}/"
            os.makedirs(mask_path, exist_ok=True)
            for i, mask_np in enumerate(masks_nps):
                mask_save_path = mask_path+f'mask{i+1}.png'
                save_mask(mask_np, mask_save_path)


if __name__ == "__main__":
    main()

