import pandas as pd
import numpy as np
import os

"""
용도 : 파일 이름 변경

코드실행 결과 : ./source/high/folder의 이미지를 이용하여
high_i의 형태를 가진 이름으로 변경

"""

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

