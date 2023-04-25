from pandas import read_csv

kpi_df = read_csv("kaggle-package-index.csv")
kpi_df = kpi_df[kpi_df["Is_Current"] == 1]

sorts = kpi_df["Sort"].unique().tolist()

with open("README.md", "w") as file:
    file.write("# Kaggle-Package-Index\n")
    file.write("## Overall:\n")
    overall_df = kpi_df.groupby("Package")["Count"].sum().reset_index()
    overall_df = overall_df.nlargest(10, "Count")
    for i, row in enumerate(overall_df.itertuples()):
        file.write("### " + str(i + 1) + ". " + row.Package + "\n")
    for option in sorts:
        file.write("#\n## By " + option + ":\n")
        sort_df = kpi_df[kpi_df["Sort"] == option]
        sort_df = sort_df.nlargest(10, "Count")
        for i, row in enumerate(sort_df.itertuples()):
            file.write(
                "### "
                + str(i + 1)
                + ". "
                + row.Package
                + " - "
                + str(row.Count)
                + " uses\n"
            )
