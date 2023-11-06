# 평가 함수들을 제공하는 모듈

import matplotlib.pyplot as plt
from sklearn.metrics import (confusion_matrix, 
                             ConfusionMatrixDisplay, 
                             recall_score, 
                             accuracy_score, 
                             precision_score, 
                             f1_score, 
                             average_precision_score, 
                             roc_auc_score, 
                             precision_recall_curve, 
                             PrecisionRecallDisplay, 
                             roc_curve, 
                             RocCurveDisplay, 
                             r2_score, 
                             mean_squared_error
                            )
def print_metrics_regression(y, pred, title=None):
    """
    회귀 평가지표를 출력하는 함수
    [parameter]
        y: ndarray - 정답
        pred: ndarray - 모델추론값
        title: 출력 제목
    """
    if title:
        print(f"============{title}============")
    print("MSE:", mean_squared_error(y, pred))
    print("RMSE:", mean_squared_error(y, pred, squared=False))
    print("R2:", r2_score(y, pred))


def plot_roc_curve(y, pos_proba, estimator_name, title=None):
    """
    Roc Curve를 시각화하는 함수
    [parameter]
        y: ndarray - 정답
        pos_proba: ndarray - 모델이 추정한 양성(positive)의 확률
        estimator_name: str - 범례(legend)에 나올 모델이름
    """
    auc_score = roc_auc_score(y, pos_proba)
    fpr, tpr, _ = roc_curve(y, pos_proba)
    RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc_score, 
                    estimator_name=estimator_name).plot()
    if title:
        plt.title(title)
    plt.show()

def plot_precision_recall_curve(y, pos_proba, estimator_name, title=None):
    """
    PrecisionRecall Curve를 시각화하는 함수
    [parameter]
        y: ndarray - 정답
        pos_proba: ndarray - 모델이 추정한 양성(positive)의 확률
        estimator_name: str - 범례(legend)에 나올 모델이름
    """
    ap_score = average_precision_score(y, pos_proba)
    precision_list, recall_list, _ = precision_recall_curve(y, pos_proba)
    PrecisionRecallDisplay(precision_list, recall_list, 
                           average_precision=ap_score, 
                           estimator_name=estimator_name).plot()
    if title:
        plt.title(title)
    plt.show()


def plot_confusion_matrix(y, pred, title=None):
    """
    confusion matrix를 시각화하는 함수
    [parameter]
        y:ndarray - 정답(ground truth)
        pred: ndarray - 모델이 추정한 값
        title: str - 그래프의 제목(title)
    """
    cm = confusion_matrix(y, pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot(cmap='Blues')
    if title:
        plt.title(title)
    plt.show()
    
def print_metrics_classification(y, pred, pos_proba=None, title=None):  
    """
    분류 평갖치표 점수들을 출력하는 함수.
    accuracy, recall, precision, f1 score 
    average precision score, roc-auc score를 출력
    [parameter]
        y:ndarray - 정답
        pred:ndarray - 모델 추정값
        pos_proba:ndarry - 모델이 추정한 Positive의 확률. 
                           default: None - ap score, auc score 는 계산하지 않는다.
        title:str - 제목
    """
    if title:
        print(f"=========={title}==========")
    print(f"정확도(Accuracy): {accuracy_score(y, pred)}")
    print(f"재현율(Recall) : {recall_score(y, pred)}")
    print(f"정밀도(Precision): {precision_score(y, pred)}")
    print(f"F1 Score: {f1_score(y, pred)}")
    if pos_proba is not None:
        print(f"AveagePrecision Score: {average_precision_score(y, pos_proba)}")
        print(f"ROC-AUC Score: {roc_auc_score(y, pos_proba)}")
