import matplotlib.pyplot as plt

def plot_against(df, name, col):
    df.groupby(name).mean()[col].plot.bar(stacked=True, figsize=(20,10))

def plot_and_save(df, name, col, path):
    plot_against(df, name, col)
    plt.savefig(path + f"/{col}-{name}")
