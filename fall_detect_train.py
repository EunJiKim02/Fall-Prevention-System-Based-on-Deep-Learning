import pandas as pd
from pycaret.classification import *
import os
import warnings

warnings.filterwarnings("ignore")


"""
용도: 정상 행동과 낙상 위험 행동 분류기 학습 및 모델 선정

코드실행 결과
앞의 과정에서 추출된 특징을 이용하여 분류기 학습 진행 

우수한 분류기를 선택 후 모델 저장
(저장경로: ./checkpoint)

"""


def fall_detect_model_train(df, path, ensemble=False, n_select=3):
    df = df.iloc[:, 1:]
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

    if not os.path.exists(path):
        os.makedirs(path)
    save_model(final_model, path)
    print()


def main():
    df = pd.read_csv("./data/train/pose/dataset.csv")
    # print(df)
    model_path = "./checkpoint/"
    fall_detect_model_train(df, model_path, ensemble=False)


if __name__ == "__main__":
    main()
