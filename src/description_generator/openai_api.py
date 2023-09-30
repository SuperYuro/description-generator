import os
from dotenv import load_dotenv
import openai


def load_openai_api_key() -> str:
    load_dotenv(".env")
    return os.getenv("OPENAI_API_KEY")


openai.api_key = load_openai_api_key()

custom_prompt: str = """
    これから，Wikipediaの記事の全文をMarkdown形式で投げます．
    回答は，下記に指定する形式で3行でで行ってください．
    記事がある特定の植物，または植物の種類の枠組み（例えば，ある属の解説など）に関する記事であった場合は，以下のように回答してください．
    - 1行目は`Plant`にする
    - 2行目は，花が咲く時期を`Spring`, `Summer`, `Autumn`, `Winter`のいずれかから1つ選択
    - 3行目は`Null`にする
    植物と関連性がない，または植物の一覧記事であった場合は，1行目を`Background`に，2行目を`Spring`に，3行目を`Null`にしてください．
    """


def print_custom_prompt(article: str):
    wikipedia_article = f"```\n{article}\n```"

    print(custom_prompt + "\n" + wikipedia_article)


def openai_api_test():
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": custom_prompt}],
    )
    return response


if __name__ == "__main__":
    print_custom_prompt("hogehoge\nfugafuga")
