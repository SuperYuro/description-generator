import requests

WIKIPEDIA_ENDPOINT = "https://ja.wikipedia.org/w/api.php"


def get_title_from_keyword(keyword: str) -> str | None:
    # APIパラメータ
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": keyword,
        "utf8": 1,
        "srlimit": 1,  # トップ1記事のみ取得
    }

    # APIリクエスト
    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    data = response.json()

    # 検索結果があるか確認
    if data["query"]["search"]:
        return str(data["query"]["search"][0]["title"])
    else:
        return None


def get_summary_from_wikipedia(title: str) -> str | None:
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "utf8": 1,
    }
    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    data = response.json()

    page = next(iter(data["query"]["pages"].values()))
    extract = page.get("extract", None)

    return extract


def get_description_from_wikipedia(title: str) -> str | None:
    # 記事の内容を取得するための新しいAPIリクエスト
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": False,
        "utf8": 1,
    }

    response = requests.get(WIKIPEDIA_ENDPOINT, params=params)
    data = response.json()

    # 記事の内容を取得
    page = next(iter(data["query"]["pages"].values()))
    extract = page.get("extract", None)

    return extract
