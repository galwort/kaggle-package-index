import pypistats

from httpx import HTTPStatusError
from matplotlib import pyplot as plt, ticker
from matplotlib.dates import MonthLocator, DateFormatter
from pandas import concat, DataFrame, read_csv, to_datetime, to_numeric
from statsmodels.tsa.arima.model import ARIMA


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
        try:
            x_df = pypistats.overall(package, total=True, format="pandas")
            if with_mirrors:
                x_df = x_df[x_df["category"] == "with_mirrors"]
            else:
                x_df = x_df[x_df["category"] == "without_mirrors"]
            x_df = x_df[["date", "downloads"]]
            x_df = x_df.assign(package=package)
            pypi_df = concat([pypi_df, x_df])
        except HTTPStatusError:
            print(f"'{package}' not on pypi")

    return pypi_df


def format_yticks(y, _):
    return "{:,.0f}k".format(y / 1000)


def plot_pypi_downloads(pypi_df):
    _, ax = plt.subplots(figsize=(16, 9))
    pypi_df["date"] = to_datetime(pypi_df["date"])
    pypi_df = pypi_df.sort_values(by=["package", "date"])
    for package in pypi_df["package"].unique():
        ax.plot(
            pypi_df[pypi_df["package"] == package]["date"],
            pypi_df[pypi_df["package"] == package]["downloads"],
            label=package,
        )
    ax.set_xlabel("Date")
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))

    ax.set_ylabel("Downloads")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_yticks))

    ax.set_title("Package Popularity Over Time")
    ax.legend()
    plt.show()


def predict_package(package_df):
    package_df["downloads"] = to_numeric(package_df["downloads"])
    package_df = package_df.set_index("date")
    package_df.index = to_datetime(package_df.index)
    package_df = package_df.resample("M").sum()
    model = ARIMA(package_df["downloads"], order=(1, 1, 1))
    model_fit = model.fit()
    prediction = model_fit.forecast()[1]

    return prediction


packages = ["langchain"]

pypi_df = get_pypi_downloads(packages)
plot_pypi_downloads(pypi_df)
print(predict_package(pypi_df))
