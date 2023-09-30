import time
from description_generator.openai_api import (
    load_openai_api_key,
    openai_api_test,
)


from description_generator.models import (
    BookItemModel,
    ItemType,
    list_to_json,
)
from description_generator.wikipedia import (
    get_description_from_wikipedia,
    get_title_from_keyword,
    get_summary_from_wikipedia,
)
from description_generator.converter import load_labels_from_csv

plants_csv_url: str = (
    "https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_plants_V1_labelmap.csv"
)
birds_csv_url: str = (
    "https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_birds_V1_labelmap.csv"
)


def main():
    plants_label: dict[int, str] = load_labels_from_csv(plants_csv_url)
    plants_items: list[BookItemModel] = []

    for i, name in plants_label.items():
        if name == "background":
            continue

        plants_title = get_title_from_keyword(name)
        # print(plants_title)

        plants_description = (
            "情報が見つかりませんでした"
            if plants_title is None
            else get_description_from_wikipedia(title=plants_title)
        )
        if plants_title is None:
            plants_title = "不明"

        time.sleep(1)

        plants_items.append(
            BookItemModel(
                name=name,
                title=plants_title,
                description=plants_description,
                item_type=ItemType.Plant,
            )
        )

        if i == 20:
            break

    serialized_items = list_to_json(plants_items)

    print(serialized_items)


def wikipedia_test():
    name = "Homo sapiens"
    article_title = get_title_from_keyword(name)
    result = get_summary_from_wikipedia(article_title)

    print(result)


if __name__ == "__main__":
    main()
