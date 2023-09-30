import json
from dataclasses import dataclass, asdict

from enum import Enum


class ItemType(Enum):
    Background = 0
    Bird = 1
    Plant = 2


class Season(Enum):
    Spring = 0
    Summer = 1
    Autumn = 2
    Winter = 3


@dataclass
class BookItemModel:
    _name: str
    _title: str
    _description: str
    _itemType: str
    _season: str

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        item_type: ItemType,
    ):
        self._name = name
        self._title = title
        self._description = description
        self._itemType = item_type.name
        self._season = Season.Spring.name

    def to_dict(self):
        return asdict(self)

    def to_json(self) -> dict[str, dict[str, str]]:
        model_dict = self.to_dict()
        name = model_dict.pop("_name")
        ret = {name: model_dict}
        return ret


def list_to_json(items: list[BookItemModel]) -> str:
    serialized_items = {}
    for item in items:
        serialized_items.update(item.to_json())

    return json.dumps(serialized_items)
