import pandas as pd

'''
용도 : 레이블과 키포인트 간의 상관행렬 분석

코드실행 결과 : 상관행렬 값이 csv 파일로 저장
'''

mode = "test"
root_path = f"./data/{mode}/pose/"
# CSV 파일 경로 설정
file_path = root_path + "dataset.csv"


# 데이터 읽기
df = pd.read_csv(file_path)
df = df.drop("Img", axis=1)


# 상관 계수 계산
correlation_matrix = df.corr()
# correlation_matrix
print("Correlation Matrix:")
print(correlation_matrix["label"])

# 상관관계 csv 파일로 저장
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
