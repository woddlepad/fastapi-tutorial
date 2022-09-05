import json
import os
from typing import Any, Dict, TypeVar
from typing_extensions import Self
from pydantic import BaseModel, Field, parse_obj_as


T = TypeVar("T")


class ClassInDB(BaseModel):
    id: str

    def save(self):
        cls_name = type(self).__name__
        os.mkdir(f"data/{cls_name}") if not os.path.exists("data/{cls_name}") else None
        with open(f"data/{cls_name}/{self.id}.json", "w") as file:
            file.write(self.json())

    @classmethod
    def read(cls: type[Self], id: str):  # type: ignore
        cls_name = cls.__name__
        with open(f"data/{cls_name}/{id}.json", "r") as file:
            class_in_db = json.load(file)
            return parse_obj_as(cls, class_in_db)

    def delete(self):
        os.remove(f"data/{self.id}.json")
