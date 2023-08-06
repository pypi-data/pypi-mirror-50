import matplotlib.pyplot as plt

def plot_against(df, name, col):
    plot_agg(df, name, col, "mean")

def plot_agg(df, name, col, agg="mean"):
    df.groupby(name).agg({col: [agg]}).plot.bar(stacked=True, figsize=(20,10))

def plot_and_save(df, name, col, path):
    plot_against(df, name, col)
    plt.savefig(path + f"/{col}-{name}")
