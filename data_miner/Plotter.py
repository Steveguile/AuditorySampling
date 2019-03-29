import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plot_dir = os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0], r"data\plots")
use_dirs = ['Test', 'Train']

def heat_map(type, dataset):
    # Correlation Matrix Heatmap
    f, ax = plt.subplots(figsize=(10, 6))

    correlation = dataset.corr()

    hm = sns.heatmap(round(correlation,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                     linewidths=.05, annot_kws={"size": 6})

    f.subplots_adjust(top=0.93)
    #f = f.suptitle(type + ' Audio Data Correlation Heatmap', fontsize=14, va="top")
    # plt.show()
    plt.savefig(os.path.join(plot_dir, type.lower()+"_heatmap.png"), bbox_inches='tight')


def pairwise_scatter(type, headers, dataset):
    # Scatter Plot
    cols = headers
    pp = sns.pairplot(dataset[cols], hue='TrafficIncident', height=1.8, aspect=1.8,
                      palette={"Yes": "#7A81A3", "No": "#76C6C9"},
                      plot_kws=dict(edgecolor="black", linewidth=0.5))

    fig = pp.fig

    fig.subplots_adjust(top=0.93, wspace=0.3)
    #f = fig.suptitle(type + 'Audio Data Pairwise Plots', fontsize=14, va="top")
    # plt.show()
    plt.savefig(os.path.join(plot_dir, type.lower()+"_scatter.png"), bbox_inches='tight')


def main():

    for dir_type in use_dirs:

        csv_file = pd.read_csv(os.path.join(os.path.dirname(__file__).rsplit("/", 1)[0],
                                            "data", dir_type.lower() + "_traffic_audio.csv"),header=0)

        csv_headers = list(csv_file.columns.values)
        dataset = csv_file.drop("reference", axis=1)
        headers = list(dataset.columns.values)
        attribute_headers = headers[0:len(headers) - 1]

        heat_map(dir_type, dataset)
        pairwise_scatter(dir_type, headers, dataset)


main()

