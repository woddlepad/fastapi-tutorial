import json
import os
from typing import Any, Dict, TypeVar
from typing_extensions import Self
from pydantic import BaseModel, Field, parse_obj_as


T = TypeVar("T")


def get_db_folder():
    return os.environ.get("DB_FOLDER", "data")


class ClassInDB(BaseModel):
    id: str

    def save(self, overwrite: bool = True):
        db_folder = get_db_folder()
        cls_name = type(self).__name__
        if not overwrite and os.path.exists(f"{db_folder}/{cls_name}/{self.id}.json"):
            raise ValueError(
                f"{cls_name} with id {self.id} already exists. choose another id"
            )
        if not os.path.exists(f"{db_folder}/{cls_name}"):
            os.mkdir(f"{db_folder}/{cls_name}")
        with open(f"{db_folder}/{cls_name}/{self.id}.json", "w") as file:
            file.write(self.json())

    @classmethod
    def read_all(cls):  # type: ignore
        cls_name = cls.__name__
        db_folder = get_db_folder()
        file_names = os.listdir(f"{db_folder}/{cls_name}")

        return [cls.read(file_name) for file_name in file_names]

    @classmethod
    def read(cls: type[Self], id: str):  # type: ignore
        cls_name = cls.__name__
        db_folder = get_db_folder()
        with open(f"{db_folder}/{cls_name}/{id}.json", "r") as file:
            class_in_db = json.load(file)
            return parse_obj_as(cls, class_in_db)

    def delete(self):
        db_folder = get_db_folder()
        os.remove(f"{db_folder}/{self.id}.json")
