from dataclasses import dataclass
from typing import Optional, ClassVar, List, Union
from datetime import datetime, date
# Заготовка под БД
# @dataclass
# class User:
#     id: [int]
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
    # id: ClassVar[int] = 0 Запасная, если не сделаю счетчик в репозитории InMemoryWorkouts
    duration: int | float
    date: str
    title: str
    SESSION: ClassVar[List[str]] = ['cardio', 'strength', 'elliptical', 'treadmill']
    
    def validate_duraton(self, duration:int|float) -> int|float:
        # Обработаем длительность тренировки
        if self.duration is None:
            raise ValueError(f'Длительность тренировки - обязательное значение')
        if not isinstance(self.duration, (int,float)):
            raise TypeError(f"Длительность должна быть числом, получен {type(self.duration)}")
        if type(self.duration) == float:
            self.duration = round(self.duration, 2)
        if self.duration <= 0:
            raise ValueError(f'Длительность не может быть <= 0')    
    
    def validate_title (self, title:str) -> str:
        # Тут мы проверяем тип тренировки из ClassVar, добавляем проверки ввода, обрабатываем ввод
        if self.title is None:
            raise ValueError(f"Введите тип тренировки")        
        elif not isinstance(self.title, str):
            raise TypeError(f'Тренировка должна быть текстом, сейчас получен {type(self.title)}')    
        # Обрабатываем ввод:
        self.title = self.title.lower().strip()
        # Проверяем допуск ClassVar
        if self.title not in self.SESSION:
            raise ValueError(f"Неверный тип тренировки: {self.title}. Допустимые: {self.SESSION}")

    def validate_date(self, date: str = "%d.%m.%Y") -> str:
    # Временное рещение, надо добавить автоматическую генерацию значения. 
    # Проверяем дату и возвращает в заданном формате
        if self.date is None:
            self.date = date.today().strftime("%d.%m.%Y")
        if isinstance(self.date, str):
            try:
                for format in ["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                    try:
                        self.date = datetime.datetime.strptime(self.date, format).date()
                        break   
                    except ValueError:
                        continue
                else:
                    ValueError(f'Не удалось распознать тип даты{self.date}')
            except Exception as e:
                raise ValueError(f'Ошибка преобразования строки в дату: {e}')                    
                               
        elif not isinstance(self.date, int):
            raise TypeError(f'Дата должна быть текстом, сейчас получен {type(self.date)}')
        # Проверяем, что дата не в будущем:
        if self.date > date.today():
           raise ValueError(f"Дата не может быть в будущем: {self.date}") 
       
    def __init__(self):
        pass

    def __post_init__(self):
        self.validate_duraton(self.duration)
        self.validate_title(self.title)
        self.validate_date(self.date)
        # self.id +=1 Запасной счетчик

# @dataclass  
# class InMemoryWorkouts:




