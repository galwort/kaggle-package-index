from pandas import read_csv

kpi_df = read_csv("kaggle-package-index.csv")
kpi_df = kpi_df[kpi_df["Is_Current"] == 1]
kpi_df = kpi_df.groupby("Package")["Count"].sum().reset_index()
kpi_df = kpi_df.nlargest(10, "Count")

with open("README.md", "w") as file:
    file.write("# Kaggle-Package-Index\n\n")
    for i, row in enumerate(kpi_df.itertuples()):
        file.write("## " + str(i + 1) + ". " + row.Package + "\n")
