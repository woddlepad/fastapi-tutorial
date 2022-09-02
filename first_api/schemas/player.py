from datetime import date
from typing import Dict
from first_api.db import ClassInDB
from pydantic import BaseModel, Field


class ThrowLog(BaseModel):
    num_scored: int = Field(ge=0)
    num_missed: int = Field(ge=0)

    @property
    def accuracy(self) -> float:
        return self.num_scored / max(self.num_scored + self.num_missed, 1)


class Player(ClassInDB):
    name: str
    throws: Dict[str, ThrowLog] = Field(default_factory=list)

    def get_thow_log(self, start_date: date, end_date: date) -> ThrowLog:
        throw_log = ThrowLog(num_scored=0, num_missed=0)
        for date_str in self.throws:
            if start_date <= date.fromisoformat(date_str) <= end_date:
                throw_log.num_scored += self.throws[date_str].num_scored
                throw_log.num_missed += self.throws[date_str].num_missed
        return throw_log


class PlayerStats(BaseModel):
    accuracy: float
    improvement_7_days: float
    throw_log: ThrowLog
