import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, make_scorer
from sklearn.model_selection import GridSearchCV, train_test_split
import warnings
from sklearn import exceptions
from tabulate import tabulate
from copy import deepcopy
import os

warnings.filterwarnings(action="ignore", category=exceptions.UndefinedMetricWarning) # If it's 0 that's fine
warnings.filterwarnings(action="ignore", category=DeprecationWarning) # Don't care for this
warnings.filterwarnings(action="ignore", category=FutureWarning) # Don't care for this


csv_path = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], "data/traffic_audio.csv")


def perform_classification(X_train, y_train, X_test, y_test, classifier, parameters, scorers, pos_label):

    # Cross-Validation
    gs = GridSearchCV(classifier,
                      param_grid=parameters,
                      scoring=scorers, cv=5, refit=False,
                      return_train_score=False)  # refit='precision' only returns best precision

    gs.fit(X_train, y_train)

    classifier_name = str(classifier).split('(')[0]
    params = gs.cv_results_.get('params')

    # Do ranking myself because in-built ones don't show results for every parameter
    cv_class_acc = list(gs.cv_results_.get('mean_test_Classificiation_Accuracy'))
    cv_class_pre = list(gs.cv_results_.get('mean_test_Precision'))
    cv_class_rec = list(gs.cv_results_.get('mean_test_Recall'))
    cv_class_fscr = list(gs.cv_results_.get('mean_test_f_score'))


    # TODO: Pretend this doesn't exist
    if len(params) == 1:

        classifier.set_params(**params[0])
        classifier.fit(X_train, y_train)
        predicted_results = classifier.predict(X_test)

        ho_class_acc = accuracy_score(y_test, predicted_results)
        ho_class_pre = precision_score(y_test, predicted_results, pos_label=pos_label)
        ho_class_rec = recall_score(y_test, predicted_results, pos_label=pos_label)
        ho_class_fscr = f1_score(y_test, predicted_results, pos_label=pos_label)

        print("x" * 100, "\n", classifier_name, '('
              , str(params).replace('\'', '').replace('[', '').replace('{', '').replace('}', '').replace(']', '').replace(':', ' =') # TODO: Disgusteng!  do regex for this later
              ,")\nx" + "x" * 99)
        print(tabulate([["Classification Accuracy", str(cv_class_acc).replace('[', '').replace(']', ''), ho_class_acc],
                        ["Precision", str(cv_class_pre).replace('[', '').replace(']', ''), ho_class_pre],
                        ["Recall", str(cv_class_rec).replace('[', '').replace(']', ''), ho_class_rec],
                        ["F-Score", str(cv_class_fscr).replace('[', '').replace(']', ''), ho_class_fscr]],
                       headers=["", "CV Score", "Holdout Score"]))


    else:
        for i, parameter in enumerate(params):

            classifier.set_params(**params[i])
            classifier.fit(X_train, y_train)
            predicted_results = classifier.predict(X_test)

            ho_class_acc = accuracy_score(y_test, predicted_results)
            ho_class_pre = precision_score(y_test, predicted_results, pos_label=pos_label)
            ho_class_rec = recall_score(y_test, predicted_results, pos_label=pos_label)
            ho_class_fscr = f1_score(y_test, predicted_results, pos_label=pos_label)

            print("x" * 100, "\n", classifier_name, '('
                  , str(parameter).replace('\'', '').replace('[', '').replace('{', '').replace('}', '').replace(']','').replace(':', ' =')
                  , ")\nx" + "x" * 99)
            print(tabulate([["Classification Accuracy", str(cv_class_acc[i]), ho_class_acc],
                            ["Precision", str(cv_class_pre[i]), ho_class_pre],
                            ["Recall", str(cv_class_rec[i]), ho_class_rec],
                            ["F-Score", str(cv_class_fscr[i]), ho_class_fscr]],
                           headers=["", "CV Score", "Holdout Score"]))



def main():

    csv_file = pd.read_csv(csv_path, header=0)
    csv_headers = list(csv_file.columns.values)
    dataset = csv_file.drop("reference", axis=1)
    headers = list(dataset.columns.values)
    attribute_headers = headers[0:len(headers) - 1]

    # Shuffle Dataset
    dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

    target = list(dataset["TrafficIncident"])
    dataset = dataset.drop("TrafficIncident", axis=1).get_values()

    classifiers = {'knn': KNeighborsClassifier(),
                   'svc': SVC(),
                   'tree': DecisionTreeClassifier()
                   }

    parameters = {'knn': {'n_neighbors': [1, 3, 5]
                          },
                  'svc': {'gamma': [0.001],
                          'C': [100.]
                          },
                  'tree': {'': []},
                  'tree': {'max_features': [5]}
                  }

    # Make own SCORERS as need different pos_label
    class_accuracy = make_scorer(accuracy_score)
    pos_label = 'Yes'
    precision = make_scorer(precision_score, pos_label=pos_label)
    recall = make_scorer(recall_score, pos_label=pos_label)
    f_score = make_scorer(f1_score, pos_label=pos_label)
    scorers = {'Classificiation_Accuracy': class_accuracy,
               'Precision': precision,
               'Recall': recall,
               'f_score': f_score
               }

    X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.4, random_state=42)

    for c_key, classifier in classifiers.items():
        for p_key, c_params in parameters.items():
            if p_key == c_key:
                perform_classification(X_train, y_train, X_test, y_test, classifier, c_params, scorers, pos_label)

main()