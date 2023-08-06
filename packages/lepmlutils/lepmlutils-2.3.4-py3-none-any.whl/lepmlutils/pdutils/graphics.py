import matplotlib.pyplot as plt
import pandas as pd

def plot_against(df, name, col):
    plot_agg(df, name, col, "mean")

def plot_agg(df, name, col, agg="mean"):
    df.groupby(name).agg({col: [agg]}).plot.bar(stacked=True, figsize=(20,10))

def plot_and_save(df, name, col, path):
    plot_against(df, name, col)
    plt.savefig(path + f"/{col}-{name}")

def qplot_against(df, name, col, bins):
    qname = f"q{name}"
    df[qname] = pd.qcut(df[name], bins)
    plot_against(df, qname, col)