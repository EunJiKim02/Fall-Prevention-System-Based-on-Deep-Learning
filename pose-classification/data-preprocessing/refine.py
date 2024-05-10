import pandas as pd

path = "data/output.csv"
df = pd.read_csv(path)

# 각 행의 -1의 개수를 세어 새로운 열을 만듭니다.
df["minus_ones_count"] = df.apply(lambda row: (row == -1).sum(), axis=1)

# -1의 개수가 적은 순으로 정렬하고 이미지 이름이 중복된 행을 제거합니다.
df_result = df.sort_values(by="minus_ones_count").drop_duplicates(
    subset="Img", keep="first"
)

# 이미지 이름을 기준으로 정렬하고 -1의 개수 열을 제거합니다.
df_result.drop(columns=["minus_ones_count"], inplace=True)
df_result = df_result.sort_values(by="Img")

# 불필요한 열을 제거합니다.
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
