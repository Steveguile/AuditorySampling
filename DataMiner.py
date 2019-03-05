import pandas as pd
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn import exceptions
import warnings
from tabulate import tabulate

# Credit to https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57

warnings.filterwarnings(action="ignore", category=exceptions.UndefinedMetricWarning) # If it's 0 that's fine

def get_accuracy_scores(classifier, actual, predicted):

    classification_accuracy = accuracy_score(actual, predicted)
    precision = precision_score(actual, predicted, pos_label="Yes")
    recall = recall_score(actual, predicted, pos_label="Yes")
    fscore = f1_score(actual, predicted, pos_label="Yes")

    print("x" * 100, "\n", classifier, "\nx" + "x" * 99)
    print(tabulate([["Classification Accuracy", classification_accuracy],
                    ["Precision", precision],
                    ["Recall", recall],
                    ["F-Score", fscore]],
                   headers=["", "Score"]))

    return classification_accuracy, precision, recall, fscore


def main():
    csv_file = pd.read_csv(r"E:\Programming\Projects\Dissertation\SyntheticDataGenerator\traffic_audio.csv", header=0)
    csv_headers = list(csv_file.columns.values)
    dataset = csv_file.drop("reference", axis=1)
    headers = list(dataset.columns.values)
    attribute_headers = headers[0:len(headers) - 1]

    #Shuffle Dataset
    dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

    target = list(dataset["TrafficIncident"])
    dataset = dataset.drop("TrafficIncident", axis=1).get_values()

    X_train, X_test, y_train, y_test = train_test_split(
        dataset, target, test_size=0.4, random_state=42)

    classifiers = [
        SVC(gamma=0.001, C=100.),
        KNeighborsClassifier(n_neighbors=3)
    ]

    for classifier in classifiers:
        classifier.fit(X_train, y_train)
        y_predict = classifier.predict(X_test)
        get_accuracy_scores(classifier, y_test, y_predict)

main()