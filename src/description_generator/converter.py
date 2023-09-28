import io

import html2text
import pandas
import requests


def html_to_markdown(html_content) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = False

    markdown_content = h.handle(html_content)

    return markdown_content


def load_labels_from_csv(label_url: str) -> dict[int, str]:
    response = requests.get(label_url)
    response.raise_for_status()

    csv_data = io.StringIO(response.text)
    df = pandas.read_csv(csv_data, delimiter=",")
    labels = df.set_index("id")["name"].to_dict()

    return labels
