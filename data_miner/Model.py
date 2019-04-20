import pickle
import os
import pandas as pd
from sklearn import tree
from pydotplus import graphviz
import numpy as np
import copy
import csv
import random
import geopip
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tabulate import tabulate
import platform
from shutil import copyfile
import errno
import time

# /Test because using holdout
audio_sub_dir = os.path.join("data", "audio", "Test")

if platform.system() == "Linux":
    dir_name = ''
    server_root = '/var/www/html'
else:
    dir_name = os.path.dirname(__file__).rsplit("/", 1)[0]
    server_root = ''

model_name = 'DecisionTreeClassifier(max_depth = 5, max_features = None, min_samples_split = 10)'
csv_path = os.path.join(dir_name, "data", "test_traffic_audio.csv")
model_path = os.path.join(dir_name, "data", "models")
out_path = os.path.join(dir_name, 'data')

file_path = os.path.join(dir_name, audio_sub_dir)

# Output Folder Names (Can be changed for anything)
no_traffic_incident = "No_Traffic_Incident"
traffic_incident = "Traffic_Incident"

def display_tree(classifier, headers, target):
    dot_data = tree.export_graphviz(classifier,
                                    out_file=None,
                                    feature_names=headers,
                                    class_names=target)

    graph = graphviz.graph_from_dot_data(dot_data)

    graph.write_png(os.path.join(out_path, model_name + '.png'))


def to_csv(file, keys, dict_list):
    with open(file, "w", newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


# Get a coordinate somewhere in UK borders
def coord_data():
    # UK borders exist somewhere between -8.5 to 2.2 (latitude) and 49.5 to 60 (longitude)
    Lat = random.uniform(49.5, 60)
    Long = random.uniform(-8.5, 2.2)
    coord = geopip.search(lat=Lat, lng=Long)

    # Fancied doing some recursion, not optimal over while loop though
    if coord is None:
        return coord_data()
    elif coord["FIPS"] == 'UK':
        return Lat, Long
    else:
        return coord_data()


def performance_measures(predicted, actual):
    pos_label = 'Yes'
    accuracy = accuracy_score(actual, predicted)
    precision = precision_score(actual, predicted, pos_label=pos_label)
    recall = recall_score(actual, predicted, pos_label=pos_label)
    f_score = f1_score(actual, predicted, pos_label=pos_label)

    print(tabulate([["Classification Accuracy", accuracy],
                    ["Precision", precision],
                    ["Recall", recall],
                    ["F-Score", f_score]],
                   headers=["", "Score"]))


def output_incorrect_predictions(dict_list):
    keys = dict_list[0].keys()
    to_csv(os.path.join(out_path, "incorrect_predictions.csv"), keys, dict_list)


def output_predictions(dict_list):
    # Predicted true
    for dict in dict_list:
        x, y = coord_data()
        dict.update({"XCoord": x, "YCoord": y})

        if os.path.isfile(os.path.join(file_path, no_traffic_incident, dict["Reference"]) + ".wav"):
            dict["Directory"] = os.path.join(audio_sub_dir, no_traffic_incident, dict["Reference"])
        else:
            dict["Directory"] = os.path.join(audio_sub_dir, traffic_incident, dict["Reference"])

        dict["FileType"] = ".wav"

        dict.pop("Actual")
        dict.pop("Predicted")

    keys = dict_list[0].keys()
    to_csv(os.path.join(out_path, "audio_files.csv"), keys, dict_list)


def move_file(current_dir, filetype):
    # Credit to usr nbro for answer on https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    copyfile(os.path.join(current_dir + filetype), os.path.join(server_root, current_dir + filetype))


def create_folders():

    # Hard code because we know what it'll look like and to save doing it thousands of times in loop
    if not os.path.exists(os.path.dirname(os.path.join(server_root, audio_sub_dir))):
        try:
            os.makedirs(os.path.join(server_root, audio_sub_dir, no_traffic_incident))
            os.makedirs(os.path.join(server_root, audio_sub_dir, traffic_incident))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def main():

    start = time.time()

    if os.path.isfile(csv_path):
        classifier = pickle.load(open(os.path.join(model_path, model_name), 'rb'))

        csv_file = pd.read_csv(csv_path, header=0)

        # Shuffle Dataset
        dataset = csv_file.sample(frac=1, random_state=42).reset_index(drop=True)

        references = dataset["reference"]
        dataset = dataset.drop("reference", axis=1)
        headers = list(dataset.columns.values)

        target = list(dataset["TrafficIncident"])
        dataset = dataset.drop("TrafficIncident", axis=1).get_values()

        headers.remove("TrafficIncident")

        display_tree(classifier, headers, np.unique(target))

        predicted = classifier.predict(dataset)

        performance_measures(predicted, target)

        reference_dict = {}
        incorrect_predictions = []
        predicted_true = []

        for i, reference in enumerate(references):
            reference_dict.update({"Reference": reference, "Actual": target[i], "Predicted": predicted[i]})

            if reference_dict["Predicted"] == 'Yes':
                predicted_true.append(copy.deepcopy(reference_dict))

            if reference_dict["Actual"] != reference_dict["Predicted"]:
                incorrect_predictions.append(copy.deepcopy(reference_dict))

        output_incorrect_predictions(incorrect_predictions)

        output_predictions(predicted_true)

        # Only for deployement, move predicted true to server root
        if platform.system() == "Linux":
            create_folders()
            for predicted in predicted_true:
                move_file(predicted["Directory"], predicted["FileType"])

    else:
        print(csv_path + "is not a valid input file")

    end = time.time()

    print('Time to classify individual file:', str(((end - start) * 100) / len(csv_file.index)) + 'ms')


main()
