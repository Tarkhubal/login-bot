import datetime
import json

from typing import Union

def get_date():
    return datetime.datetime.now()

def datetime_to_unix(date: datetime.datetime) -> int:
    return int(date.timestamp())

def unix_to_datetime(date: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(date)

def thisdate_to_unix():
    return datetime_to_unix(get_date())

def get_config() -> dict:
    with open("configs.json", "r") as file:
        return json.load(file)

def listplural(data: Union[list, int], word: str = "") -> str:
    if isinstance(data, int):
        return f"{word}{'s' if data > 1 else ''}"
    return f"{word}{'s' if len(data) > 1 else ''}"

def pl(data: Union[list, int], word: str = "") -> str:
    return listplural(data, word)