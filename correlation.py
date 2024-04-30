import pandas as pd

# CSV 파일 경로 설정
# file_path = "./data/train/pose/dataset.csv"
file_path = "output_test.csv"


# 데이터 읽기
df = pd.read_csv(file_path)
df = df.drop("Img", axis=1)


# 상관 계수 계산
correlation_matrix = df.corr()
# correlation_matrix
print("Correlation Matrix:")
print(correlation_matrix["label"])

# 상관관계 csv 파일로 저장
correlation_matrix.to_csv("./correlation_matrix.csv")
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
