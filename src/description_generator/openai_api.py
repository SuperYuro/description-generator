import os
from dotenv import load_dotenv


def get_api_key_from_env() -> str:
    load_dotenv(".env")

    return os.getenv("OPENAI_API_KEY")
