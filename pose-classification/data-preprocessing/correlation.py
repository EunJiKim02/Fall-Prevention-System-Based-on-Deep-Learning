import pandas as pd

"""
용도 : 레이블과 키포인트 간의 상관행렬 분석

코드실행 결과 : ./data/{mode}/pose/dataset.csv의 데이터셋을 이용하여
계산한 상관행렬 값이 ./data/{mode}/pose/correlation.csv 파일로 저장

"""

mode = "test"
root_path = f"./data/{mode}/pose/"
file_path = root_path + "dataset.csv"


df = pd.read_csv(file_path)
df = df.drop("Img", axis=1)


correlation_matrix = df.corr()

print("Correlation Matrix:")
print(correlation_matrix["label"])

correlation_matrix.to_csv(root_path+"correlation_matrix.csv")
[
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
]
