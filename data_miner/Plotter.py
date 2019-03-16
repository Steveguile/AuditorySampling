import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


csv_file = pd.read_csv(r"E:\Programming\Projects\Dissertation\SyntheticDataGenerator\traffic_audio.csv", header=0)
csv_headers = list(csv_file.columns.values)
dataset = csv_file.drop("reference", axis=1)
headers = list(dataset.columns.values)
attribute_headers = headers[0:len(headers)-1]

def heat_map():
    # Correlation Matrix Heatmap
    f, ax = plt.subplots(figsize=(10, 6))

    correlation = dataset.corr()

    hm = sns.heatmap(round(correlation,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                     linewidths=.05, annot_kws={"size": 6})

    f.subplots_adjust(top=0.93)
    # f = f.suptitle('Audio Data Correlation Heatmap', fontsize=14, va="top") Ignore title for now

    plt.show()

def pairwise_scatter():
    # Scatter Plot
    cols = headers
    pp = sns.pairplot(dataset[cols], hue='TrafficIncident', height=1.8, aspect=1.8,
                      palette={"Yes": "#7A81A3", "No": "#76C6C9"},
                      plot_kws=dict(edgecolor="black", linewidth=0.5))

    fig = pp.fig

    fig.subplots_adjust(top=0.93, wspace=0.3)
    # f = fig.suptitle('Wine Attributes Pairwise Plots', fontsize=14)

    plt.show()
