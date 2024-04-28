import pandas as pd
import numpy as np
import os

source_path = "./data/crop"

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

