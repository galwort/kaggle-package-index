import pypistats

from matplotlib import pyplot as plt
from pandas import concat, DataFrame, read_csv


def get_kaggle_packages(packages=5, sort="all"):
    kpi_df = read_csv("kaggle-package-index.csv")
    kpi_df = kpi_df[kpi_df["Is_Current"] == 1]
    if sort != "all":
        kpi_df = kpi_df[kpi_df["Sort"] == sort]
    else:
        kpi_df = kpi_df.groupby("Package")["Count"].sum().reset_index()
    kpi_df = kpi_df.nlargest(packages, "Count")

    return kpi_df["Package"].tolist()


def get_pypi_downloads(packages, with_mirrors=True):
    pypi_df = DataFrame(columns=["package", "date", "downloads"])
    for package in packages:
        x_df = pypistats.overall(package, total=True, format="pandas")
        if with_mirrors:
            x_df = x_df[x_df["category"] == "with_mirrors"]
        else:
            x_df = x_df[x_df["category"] == "without_mirrors"]
        x_df = x_df[["date", "downloads"]]
        x_df = x_df.assign(package=package)
        pypi_df = concat([pypi_df, x_df])

    return pypi_df


def plot_pypi_downloads(pypi_df):
    fig, ax = plt.subplots(figsize=(16, 9))
    for package in pypi_df["package"].unique():
        ax.plot(
            pypi_df[pypi_df["package"] == package]["date"],
            pypi_df[pypi_df["package"] == package]["downloads"],
            label=package,
        )
    ax.legend()
    plt.show()


plot_pypi_downloads(get_pypi_downloads(get_kaggle_packages()))
