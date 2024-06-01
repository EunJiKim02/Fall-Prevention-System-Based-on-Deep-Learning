import os
import random
import shutil

# data split
source_path = "./source"
train_path = "./train/src"
test_path = "./test/src"

for folder in os.listdir(source_path):
    img_list = os.listdir(os.path.join(source_path, folder))
    img_list = [img for img in img_list if img.endswith(".jpg")]
    random.shuffle(img_list)
    train_list = img_list[: int(len(img_list) * 0.8)]
    test_list = img_list[int(len(img_list) * 0.8) :]

    for img in train_list:
        shutil.copy(
            os.path.join(source_path, folder, img), os.path.join(train_path, img)
        )
    for img in test_list:
        shutil.copy(
            os.path.join(source_path, folder, img), os.path.join(test_path, img)
        )
