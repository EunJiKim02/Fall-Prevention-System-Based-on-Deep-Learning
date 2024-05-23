import pandas as pd

"""
용도 : 레이블 삭제

코드실행 결과 : ./data/output.csv의 데이터셋을 이용하여 
키포인트와 상관관계가 없는 레이블 삭제 후 ./data/output_refined.csv 파일로 저장

"""

path = "data/output.csv"
df = pd.read_csv(path)

df["minus_ones_count"] = df.apply(lambda row: (row == -1).sum(), axis=1)

df_result = df.sort_values(by="minus_ones_count").drop_duplicates(
    subset="Img", keep="first"
)

df_result.drop(columns=["minus_ones_count"], inplace=True)
df_result = df_result.sort_values(by="Img")

df_result = df_result.drop(
    [
        "NoseX",
        "NoseY",
        "REyeX",
        "REyeY",
        "LEyeX",
        "LEyeY",
        "REarX",
        "REarY",
        "LEarX",
        "LEarY",
    ],
    axis=1,
)


df_result.to_csv("data/output_refined.csv", index=False)
