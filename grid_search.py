import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

def custom_clf_report(y_test, y_test_pred):
    print(f'Accuracy Score: {accuracy_score(y_test, y_test_pred)}')
    print(f'Precision Score: {precision_score(y_test, y_test_pred)}')
    print(f'Recall Score: {recall_score(y_test, y_test_pred)}')
    print(f'F1 Score: {f1_score(y_test, y_test_pred)}')
    cm = confusion_matrix(y_test, y_test_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negative", "Positive"])
    disp.plot()
    
def experiment(
    X_train, y_train, X_test, y_test, 
    param_grid = {"C": [0.1, 1, 10]}
):
    # setup
    np.random.seed(12345)
    svc = SVC(class_weight="balanced")

    # run grid search
    classifier = GridSearchCV(svc, param_grid, verbose=3).fit(X_train, y_train)
    params = classifier.best_params_
    preds = classifier.best_estimator_.predict(X_test)

    # prin params and classification report
    print(f'Best Params" {params}')
    print(classification_report(y_test, preds))

    # show confusion matrix
    cm = confusion_matrix(y_test, y_test_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negative", "Positive"])
    disp.plot()
