import pandas as pd
from pycaret.classification import *  # type: ignore
import os
import warnings

warnings.filterwarnings("ignore")


"""
용도: 정상 행동과 낙상 위험 행동 분류기 train 및 모델 선정

코드실행 결과
./data/{mode}/pose/dataset.csv의 데이터셋을 이용하여 
정상 행동과 낙상 위험 행동에 대한 분류를 학습 후 선택하여 ./checkpoint/pkl 파일로 저장

"""


def fall_detect_model_train(df, save_path, ensemble=False, n_select=3):
    df = df.iloc[:, 1:]  # img_name 제외
    # print(df)
    clf = setup(
        data=df,
        target="label",
        fold=3,
        index=False,
        use_gpu=False,
        session_id=777,
        verbose=True,
    )
    model = compare_models(sort="Accuracy", fold=3, n_select=1, verbose=True)
    if ensemble:
        best_models = compare_models(
            sort="Accuracy",
            fold=5,
            n_select=n_select,
            verbose=True,
            exclude=["ridge", "sgd"],
        )

        best_tune_models = [
            tune_model(m, optimize="Accuracy", n_iter=10) for m in best_models
        ]
        model = stack_models(
            estimator_list=best_tune_models,
            meta_model=model,
            fold=3,
            method="auto",
            restack=True,
            verbose=True,
        )

    tuned_model = tune_model(model, optimize="Accuracy", n_iter=10)

    final_model = finalize_model(tuned_model)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_model(final_model, save_path)
    print()


def main():
    csv_file = "./data/train/pose/dataset.csv"
    df = pd.read_csv(csv_file)
    print(df)
    save_model_path = "./checkpoint/"
    fall_detect_model_train(df, save_model_path, ensemble=False)


if __name__ == "__main__":
    main()
