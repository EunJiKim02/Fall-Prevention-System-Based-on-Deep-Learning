import pandas as pd
import numpy as np
import os

source_path = "./source"

for high in os.listdir(source_path):
    print(high)
    i = 0
    for folder in os.listdir(os.path.join(source_path, high)):
        print(folder)
        for img in os.listdir(os.path.join(source_path, high, folder)):
            img_path = os.path.join(source_path, high, folder, img)
            print(img_path)
            os.rename(
                img_path, os.path.join(source_path, high, folder, f"{high}_{i}.jpg")
            )
            i += 1

# # data split
# train_path = "./train"
# test_path = "./test"

# for folder in os.listdir(source_path):
#     img_list = os.listdir(os.path.join(source_path, folder))

#     train_list = img_list[: int(len(img_list) * 0.8)]
#     test_list = img_list[int(len(img_list) * 0.8) :]

#     for img in train_list:
#         os.rename(os.path.join(source_path, folder, img), os.path.join(train_path, img))
#     for img in test_list:
#         os.rename(os.path.join(source_path, folder, img), os.path.join(test_path, img))
