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
    param_grid = {"C": [0.1, 1, 10]},
    model = SVC(class_weight="balanced"),
    **kwargs
):
    """
    Run a single experiment, printing 

    --- Parameters ---
    X_train, y_train, X_test, y_test: training and testing features and labels
    
    param_grid: the grid of paramaters to pass to GridSearchCV; 
        defaults to {"C": [0.1, 1, 10]}

    model: the model to be passed to GridSearchCV as the estimator
        defaults to SVC(class_weight="balanced")

    **kwargs: keyword arguments are passed to GridSearchCV
    """
    # run grid search
    classifier = GridSearchCV(model, param_grid, verbose=1, **kwargs).fit(X_train, y_train)
    params = classifier.best_params_
    preds = classifier.best_estimator_.predict(X_test)

    # prin params and classification report
    print(f'Best Params" {params}')
    print(classification_report(y_test, preds))

    # show confusion matrix
    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Negative", "Positive"])
    disp.plot()
