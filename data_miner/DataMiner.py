import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, make_scorer
from sklearn.model_selection import GridSearchCV, train_test_split
import warnings
from sklearn import exceptions
from tabulate import tabulate
import os
import pickle
from collections import OrderedDict
import copy
import csv

warnings.filterwarnings(action="ignore", category=exceptions.UndefinedMetricWarning) # If it's 0 that's fine
warnings.filterwarnings(action="ignore", category=DeprecationWarning) # Don't care for this
warnings.filterwarnings(action="ignore", category=FutureWarning) # Don't care for this


csv_path = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], "data/traffic_audio.csv")
model_path = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], "data/models/")
performance_path = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], "data/performance_scores.csv")

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

    performance_dict = {}
    # For Classifiers with more than one set of parameters
    param_dict = {}
    param_list = []


    # TODO: Maybe make this a bit prettier
    if len(params) == 1:

        classifier.set_params(**params[0])
        classifier.fit(X_train, y_train)
        predicted_results = classifier.predict(X_test)

        ho_class_acc = accuracy_score(y_test, predicted_results)
        ho_class_pre = precision_score(y_test, predicted_results, pos_label=pos_label)
        ho_class_rec = recall_score(y_test, predicted_results, pos_label=pos_label)
        ho_class_fscr = f1_score(y_test, predicted_results, pos_label=pos_label)

        # This may be ugly but fastest way according to Hugo on https://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
        classifier_with_params = classifier_name + '(' + str(params).replace('\'', '').replace('[', '').replace('{','').replace('}', '').replace(']', '').replace(':', ' =') + ')'

        print("x" * 100, "\n"+ classifier_with_params, "\nx" + "x" * 99)
        print(tabulate([["Classification Accuracy", str(cv_class_acc).replace('[', '').replace(']', ''), ho_class_acc],
                        ["Precision", str(cv_class_pre).replace('[', '').replace(']', ''), ho_class_pre],
                        ["Recall", str(cv_class_rec).replace('[', '').replace(']', ''), ho_class_rec],
                        ["F-Score", str(cv_class_fscr).replace('[', '').replace(']', ''), ho_class_fscr]],
                       headers=["", "CV Score", "Holdout Score"]))

        performance_dict['Classifier'] = classifier_with_params
        performance_dict.update({'CV_CA': cv_class_acc[0], 'CV_P': cv_class_pre[0], 'CV_R': cv_class_rec[0], 'CV_F': cv_class_fscr[0],
                                 'CV_Tot': cv_class_acc[0] + cv_class_pre[0] + cv_class_rec[0] + cv_class_fscr[0],
                                 'HO_CA': ho_class_acc, 'HO_P': ho_class_pre, 'HO_R': ho_class_rec, 'HO_F': ho_class_fscr,
                                 'HO_Tot': ho_class_acc + ho_class_pre + ho_class_rec + ho_class_fscr})

        param_dict['i'] = -1
        param_dict['Content'] = performance_dict
        param_list.append(copy.deepcopy(param_dict))

        pickle.dump(classifier, open(model_path + classifier_with_params, 'wb'))


    else:
        for i, parameter in enumerate(params):

            classifier.set_params(**params[i])
            classifier.fit(X_train, y_train)
            predicted_results = classifier.predict(X_test)

            ho_class_acc = accuracy_score(y_test, predicted_results)
            ho_class_pre = precision_score(y_test, predicted_results, pos_label=pos_label)
            ho_class_rec = recall_score(y_test, predicted_results, pos_label=pos_label)
            ho_class_fscr = f1_score(y_test, predicted_results, pos_label=pos_label)

            classifier_with_params = classifier_name + '(' + str(parameter).replace('\'', '').replace('[', '').replace('{', '').replace('}', '').replace(']','').replace(':', ' =') + ')'

            print("x" * 100, "\n" + classifier_with_params, "\nx" + "x" * 99)
            print(tabulate([["Classification Accuracy", str(cv_class_acc[i]), ho_class_acc],
                            ["Precision", str(cv_class_pre[i]), ho_class_pre],
                            ["Recall", str(cv_class_rec[i]), ho_class_rec],
                            ["F-Score", str(cv_class_fscr[i]), ho_class_fscr]],
                           headers=["", "CV Score", "Holdout Score"]))

            performance_dict['Classifier'] = classifier_with_params
            performance_dict.update({'CV_CA': cv_class_acc[i],
                                     'CV_P': cv_class_pre[i],
                                     'CV_R': cv_class_rec[i],
                                     'CV_F': cv_class_fscr[i],
                                     'CV_Tot': cv_class_acc[i] + cv_class_pre[i] + cv_class_rec[i] + cv_class_fscr[i],
                                     'HO_CA': ho_class_acc,
                                     'HO_P': ho_class_pre,
                                     'HO_R': ho_class_rec,
                                     'HO_F': ho_class_fscr,
                                     'HO_Tot': ho_class_acc + ho_class_pre + ho_class_rec + ho_class_fscr})

            param_dict['i'] = i
            param_dict['Content'] = performance_dict
            param_list.append(copy.deepcopy(param_dict))

            pickle.dump(classifier, open(model_path + classifier_with_params, 'wb'))

    return param_list


def main():

    csv_file = pd.read_csv(csv_path, header=0)
    dataset = csv_file.drop("reference", axis=1)

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
                  'tree': {'max_features': [None, 5, 7],
                           'max_depth': [None, 5, 10, 15],
                           'min_samples_split': [2, 4, 7, 10]}
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

    result_list = []
    output_list = []

    for c_key, classifier in classifiers.items():
        for p_key, c_params in parameters.items():
            if p_key == c_key:
                result = perform_classification(X_train, y_train, X_test, y_test, classifier, c_params, scorers, pos_label)
                result_list.append(result)

    for result in result_list:
        if result[0].get('i') == -1: # - 1 default for one-time used classifiers (1 set of params)
            output_list.append(copy.deepcopy(result[0].get('Content')))
        else:
            for my_list in result:
                output_list.append(copy.deepcopy(result[my_list.get('i')].get('Content')))

    dict_keys = output_list[0].keys()

    with open(os.path.join(performance_path), "w", newline='') as f:
        dict_writer = csv.DictWriter(f, dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(output_list)


main()