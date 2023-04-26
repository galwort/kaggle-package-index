import kaggle

from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame, read_csv, Series
from requests import exceptions, get
from time import sleep
from tqdm import tqdm

kaggle.api.authenticate()

csv_df = read_csv("kaggle_package_index.csv")
csv_df["Is_Current"] = 0
csv_df.to_csv("kaggle_package_index.csv", index=False, lineterminator="\n")

max_retries = 5
wait_time = 3
page_size = 100
sort_list = [
    "hotness",
    "commentCount",
    "dateCreated",
    "scoreDescending",
    "viewCount",
    "voteCount",
]

for sort in sort_list:
    from_list = []
    page = 1
    kernel_list = kaggle.api.kernels_list_with_http_info(
        page=page, page_size=page_size, language="python", sort_by=sort
    )
    kernel_len = len(kernel_list[0])

    while kernel_len > 0:
        with tqdm(total=kernel_len, desc=f"Page {page} for {sort}") as pbar:
            for i in range(page_size):
                kernel_url = "https://www.kaggle.com/code/" + kernel_list[0][i]["ref"]
                for attempt in range(max_retries):
                    try:
                        kernel_data = get(kernel_url)
                        break
                    except (exceptions.ConnectionError, exceptions.Timeout):
                        sleep(wait_time)
                else:
                    raise ConnectionError(
                        f"Failed to connect to {kernel_url} after {max_retries} attempts."
                    )
                kernel_soup = BeautifulSoup(kernel_data.text, "html.parser")

                render_soup = kernel_soup.find_all(
                    "script", {"class": "kaggle-component"}
                )
                render_text = render_soup[0].text
                if "renderedOutputUrl" not in render_text:
                    continue
                render_start = render_text.find("renderedOutputUrl") + 20
                render_end = render_text[render_start:].find('",') + render_start
                render_url = render_text[render_start:render_end]

                for attempt in range(max_retries):
                    try:
                        notebook_data = get(render_url)
                        break
                    except (exceptions.ConnectionError, exceptions.Timeout):
                        sleep(wait_time)
                else:
                    raise ConnectionError(
                        f"Failed to connect to {render_url} after {max_retries} attempts."
                    )
                notebook_soup = BeautifulSoup(notebook_data.text, "html.parser")
                notebook_set = set()
                for div in notebook_soup.find_all(
                    "div",
                    {"class": ["highlight hl-ipython3", "highlight hl-lexer_wrapper"]},
                ):
                    import_text = [
                        x.text for x in div.find_all("span", {"class": "kn"})
                    ]
                    if "import" in import_text:
                        library_text = [
                            x.text
                            for x in div.find_all(
                                "span", {"class": ["k", "kn", "n", "nn"]}
                            )
                        ]
                        from_switch = False
                        for i, word in enumerate(library_text):
                            if word == "from":
                                if "." in library_text[i + 1]:
                                    notebook_set.add(library_text[i + 1].split(".")[0])
                                else:
                                    notebook_set.add(library_text[i + 1])
                                from_switch = not from_switch
                            if word == "import":
                                if from_switch:
                                    from_switch = not from_switch
                                elif not from_switch:
                                    if "." in library_text[i + 1]:
                                        notebook_set.add(
                                            library_text[i + 1].split(".")[0]
                                        )
                                    else:
                                        notebook_set.add(library_text[i + 1])

                from_list.extend(notebook_set)
                pbar.update(1)

            page += 1
            kernel_list = kaggle.api.kernels_list_with_http_info(
                page=page, page_size=page_size, language="python", sort_by=sort
            )
            kernel_len = len(kernel_list[0])

    lib_series = Series(from_list)
    lib_counts_df = DataFrame(
        {
            "Package": lib_series,
            "Count": lib_series.groupby(lib_series).transform("count"),
        }
    )
    lib_counts_unique_df = lib_counts_df.drop_duplicates().reset_index(drop=True)
    lib_sorted_df = lib_counts_unique_df.sort_values(
        by="Count", ascending=False
    ).reset_index(drop=True)
    lib_csv_df = lib_sorted_df.assign(Sort=sort, Timestamp=datetime.now(), Is_Current=1)
    with open("kaggle_package_index.csv", "a") as f:
        lib_csv_df.to_csv(f, header=f.tell() == 0, index=False, lineterminator="\n")
