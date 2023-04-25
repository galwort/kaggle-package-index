from pandas import read_csv
import pypistats


def get_kaggle_packages(packages=5, sort="all"):
    kpi_df = read_csv("kaggle-package-index.csv")
    kpi_df = kpi_df[kpi_df["Is_Current"] == 1]
    if sort != "all":
        kpi_df = kpi_df[kpi_df["Sort"] == sort]
    else:
        kpi_df = kpi_df.groupby("Package")["Count"].sum().reset_index()
    kpi_df = kpi_df.nlargest(packages, "Count")

    return kpi_df["Package"].tolist()


print(get_kaggle_packages(packages=10, sort="hotness"))
