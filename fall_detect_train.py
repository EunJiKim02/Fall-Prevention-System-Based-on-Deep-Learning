import pandas as pd 
from pycaret.classification import *
from pycaret.anomaly import *
import os
import warnings
warnings.filterwarnings("ignore")


'''
용도: 정상 행동과 낙상 위험 행동 분류기 학습 및 모델 선정

코드실행 결과
앞의 과정에서 추출된 특징을 이용하여 분류기 학습 진행 

우수한 분류기를 선택 후 모델 저장
(저장경로: ./fall_detect_model)

'''



def fall_detect_model_train(df,path,ensemble = False,n_select=3):
    train = df
    train = train.drop(columns=['img'])

    clf = setup(data = train, target = 'label',fold=5,index=False,use_gpu=False,session_id=777,verbose=True) # 예측 값 및 학습 데이터 설정
    model = compare_models(sort='F1', fold = 5, n_select=1,verbose=True) # 가장 성능이 좋은 모델을 선정
    if ensemble:
        best_models = compare_models(sort='F1', fold = 5, n_select = n_select,verbose=True)
        model = blend_models(estimator_list =  best_models,
                       fold = 5,
                       method = 'soft',
                       optimize='F1',
                       )

    
    final_model = finalize_model(model)
    
    # 모델 저장 경로가 존재하는지 확인하고, 없다면 생성
    if not os.path.exists(path):
        os.makedirs(path)
    save_model(final_model,path)
    print()

def main():
    df = pd.read_csv('./data/train/csv/fall_detect.csv')
    model_path = './fall_detect_model/'
    fall_detect_model_train(df,model_path)
   

if __name__ == "__main__":
    main()