from pandas import read_csv
from requests import get

kpi_df = read_csv("kaggle-package-index.csv")
kpi_df = kpi_df[kpi_df["Is_Current"] == 1]

sorts = kpi_df["Sort"].unique().tolist()


def pypi_exists(package):
    return get("https://pypi.org/project/" + package).status_code == 200


with open("README.md", "w") as file:
    file.write("# Kaggle-Package-Index\n")
    file.write("## Overall:\n")
    overall_df = kpi_df.groupby("Package")["Count"].sum().reset_index()
    overall_df = overall_df.nlargest(10, "Count")
    for i, row in enumerate(overall_df.itertuples()):
        if pypi_exists(row.Package):
            package_str = (
                "[" + row.Package + "](https://pypi.org/project/" + row.Package + ")"
            )
        else:
            package_str = row.Package
        file.write("### " + str(i + 1) + ". " + package_str + "\n")
    for option in sorts:
        file.write("#\n## By " + option + ":\n")
        sort_df = kpi_df[kpi_df["Sort"] == option]
        sort_df = sort_df.nlargest(10, "Count")
        for i, row in enumerate(sort_df.itertuples()):
            if pypi_exists(row.Package):
                package_str = (
                    "["
                    + row.Package
                    + "](https://pypi.org/project/"
                    + row.Package
                    + ")"
                )
            else:
                package_str = row.Package
            file.write(
                "### "
                + str(i + 1)
                + ". "
                + package_str
                + " - "
                + str(row.Count)
                + " uses\n"
            )
