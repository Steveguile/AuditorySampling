import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score,make_scorer
from sklearn.model_selection import GridSearchCV
import warnings
from sklearn import exceptions
from sklearn.svm import SVC
from tabulate import tabulate
from copy import deepcopy

warnings.filterwarnings(action="ignore", category=exceptions.UndefinedMetricWarning) # If it's 0 that's fine

csv_path = r"E:\Programming\Projects\Dissertation\SyntheticDataGenerator\traffic_audio.csv"


def perform_cv(dataset, target, classifier, parameters, scorers):
    gs = GridSearchCV(classifier,
                      param_grid=parameters,
                      scoring=scorers, cv=5, refit=False,
                      return_train_score=False)  # refit='precision' only returns best precision

    gs.fit(dataset, target)

    classifier_name = str(classifier).split('(')[0]
    params = gs.cv_results_.get('params')

    # Do ranking myself because in-built ones don't show results for every parameter
    class_acc = list(gs.cv_results_.get('mean_test_Classificiation_Accuracy'))
    class_pre = list(gs.cv_results_.get('mean_test_Precision'))
    class_rec = list(gs.cv_results_.get('mean_test_Recall'))
    class_fscr = list(gs.cv_results_.get('mean_test_f_score'))

    classifier_stats = []

    # TODO: Pretend this doesn't exist
    if len(params) == 1:
        print("x" * 100, "\n", classifier_name, '('
              , str(params).replace('\'', '').replace('[', '').replace('{', '').replace('}', '').replace(']', '').replace(':', ' =') # TODO: Disgusteng!  do regex for this later
              ,")\nx" + "x" * 99)
        print(tabulate([["Classification Accuracy", str(class_acc).replace('[', '').replace(']', '')],
                        ["Precision", str(class_pre).replace('[', '').replace(']', '')],
                        ["Recall", str(class_rec).replace('[', '').replace(']', '')],
                        ["F-Score", str(class_fscr).replace('[', '').replace(']', '')]],
                       headers=["", "Score"]))


    else:
        for i, parameter in enumerate(params):
            print("x" * 100, "\n", classifier_name, '('
                  , str(parameter).replace('\'', '').replace('[', '').replace('{', '').replace('}', '').replace(']','').replace(':', ' =')
                  , ")\nx" + "x" * 99)
            print(tabulate([["Classification Accuracy", str(class_acc[i])],
                            ["Precision", str(class_pre[i])],
                            ["Recall", str(class_rec[i])],
                            ["F-Score", str(class_fscr[i])]],
                           headers=["", "Score"]))



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
                   'svc': SVC()
                   }

    parameters = {'knn': {'n_neighbors': [1, 3, 5]
                          },
                  'svc': {'gamma': [0.001],
                          'C': [100.]
                          }
                  }

    # Make own SCORERS as need different pos_label
    class_accuracy = make_scorer(accuracy_score)
    precision = make_scorer(precision_score, pos_label='Yes')
    recall = make_scorer(recall_score, pos_label='Yes')
    f_score = make_scorer(f1_score, pos_label='Yes')
    scorers = {'Classificiation_Accuracy': class_accuracy,
               'Precision': precision,
               'Recall': recall,
               'f_score': f_score
               }

    for c_key, classifier in classifiers.items():
        for p_key, c_params in parameters.items():
            if p_key == c_key:
                perform_cv(dataset, target, classifier, c_params, scorers)

main()