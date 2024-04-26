from PIL import Image, ImageOps
import random
import os
from tqdm import tqdm

def rotate_image_randomly(image_path,name, save_path):
    img = Image.open(image_path)
    random_degrees = random.randint(10, 30)
    rotated_img = img.rotate(random_degrees, expand=True)
    
    if random.choice([True, False]):
        final_img = ImageOps.mirror(rotated_img)
    else:
        final_img = rotated_img

    final_img.save(f"{save_path}{name}","JPEG")


def main():
    mode='train'
    root_path = f'./data/{mode}/origin/'
    folder_names = os.listdir(root_path)
    


    for folder_name in folder_names:
        img_list=os.listdir(os.path.join(root_path, folder_name))
        risk_or_normal=folder_name

        save_path = f'./data/{mode}/agumentation/{risk_or_normal}/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for img_name in tqdm(img_list):
            img_path=os.path.join(root_path, folder_name, img_name)
            print(img_path)
            rotate_image_randomly(img_path, img_name, save_path)   

if __name__ == "__main__":
    main()