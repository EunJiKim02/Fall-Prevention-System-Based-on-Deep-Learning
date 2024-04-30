import pandas as pd
import os
from sklearn.metrics import accuracy_score, recall_score, f1_score
from pycaret.classification import *
import warnings
import pandas as pd

warnings.filterwarnings("ignore")


"""
용도: 정상 행동과 낙상 위험 행동 분류 모델 평가

코드실행 결과
./fall_detect_model 폴더에 저장된 모델을 이용하여 정상 행동과 낙상 위험 행동에 대한 분류 진행
결과 값을 csv파일로 저장 
(저장 경로: ./result/)

"""


def fall_detect_predict(csv_file, model_path, save_path, gt_csvfile=None):
    pred_df = pd.read_csv(csv_file)
    if gt_csvfile:
        gt_df = pd.read_csv(gt_csvfile)
        gtlist = gt_df["label"].to_list()
    else:
        gtlist = pred_df["label"].tolist()
        test_df = pred_df.drop(columns=["label"])

    final_model = load_model(model_path)
    pred_list = predict_model(final_model, test_df)["prediction_label"].to_list()
    pred_df["pred"] = pred_list

    save_csv_path = os.path.join(save_path, "result.csv")
    pred_df.to_csv(save_csv_path, index=False)

    accuracy = accuracy_score(gtlist, pred_list)
    accuracy *= 100

    recall = recall_score(gtlist, pred_list, average="macro")
    recall *= 100

    f1score = f1_score(gtlist, pred_list, average="macro")
    f1score *= 100

    print(f"accuracy : {accuracy:.2f}")
    print(f"recall : {recall:.2f}")
    print(f"f1score : {f1score:.2f}")


def main():
    csv_file = "./data/test/pose/dataset.csv"
    model_path = "./checkpoint/"
    result_path = "./result"
    fall_detect_predict(csv_file, model_path, result_path)


if __name__ == "__main__":
    main()
