from dataclasses import dataclass
from typing import Optional, ClassVar, List
from datetime import datetime as dt,
from datetime import date
# Заготовка под БД
# @dataclass
# class User:
#     id: Optional[int]
#     first_name: Optional[str]
#     last_name: Optional[str]
#     email: Optional[str]
#     tg_id: Optional[str]
#     mobile_number: Optional[str]
#     age: Optional[int] = None
#     weight: Optional[float] = None
#     group_id: Optional[int] = None
#     created_at: Optional[dt] = None

@dataclass
class Workout:
    id: int
    date: None
    KIND_VAR: ClassVar[List[str]] = ['cardio', 'strength', 'elliptical', 'treadmill']

    kind: str

    def __post_init__(self):
        self.kind = self.kind.lower()
        if self.kind not in self.KIND_VAR:
             raise ValueError(f"Неверный тип тренировки: {self.kind}. Допустимые: {self.KIND_VAR}")

    def formatted_date(self, fmt: str = "%d.%m.%Y") -> str:
        """Возвращает дату в заданном формате"""
        return self.date.strftime(fmt)

class InMemoryWorkouts:
    def __init__(self, workout: Workout):
    next_id: int = 0

    def record_workout(self, workout: Workout):
    action = {next_id : Workout}



    def __init__(self):
        pass
    def create(self):

    def get(self):

    def list(self):

    def delete(self):




