from dataclasses import dataclass, field
from typing import ClassVar, Iterable, Optional
from datetime import datetime, date as Date
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

def _moscow_dtnow_formatted():
    return datetime.now(MOSCOW_TZ).strftime("%d.%m.%Y, %H:%M")

@dataclass(slots=True)
class User:
    tg_id: str
    created_at: str = field (default_factory=_moscow_dtnow_formatted()) 
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[int] = None

    def __post_init__(self):
        self._check_tg_id()

    @staticmethod
    def _check_tg_id(value: str):
        if self.tg_id.strip() is None:
            raise ValueError(f'Missing Telegram ID')
        if self.tg_id is not isinstance(value, str):
            raise TypeError(f"Telegram ID must be a string, now got {type(value)}")
        # Later to add check on unique tg_id    

@dataclass(slots=True)
class Exercise:
    ALLOWED_KINDS: ClassVar[tuple[str, ...]] = ('cardio', 'strength', 'other')
    kind: str # Тип упражнения
    title: str # Человекочитаемое название
    weight_kg: float 
    duration_min: float
    pace: float
    reps: int
    sets: int
    date: str
    duration_min: float
    notes: Optional[str]

    def __post_init__(self):
        pass    
    
    @staticmethod
    def kind_check():
        pass

    @staticmethod
    def get    

    # @staticmethod
    def _normalize_duraton(self, value=duration_min) -> float:
        if not isinstance(value, float):
            if type(value) == int:
                self.duration_min = float(value)
            else:
                raise TypeError(f"duration must be float, got {type(value)}")
        if self.duration_min <= 0:
            raise ValueError(f"duration must be positive, got {type(value)}")  
        self.duration_min = round(float(value), 2)
        return self.duration_min


    
    @staticmethod
    def _validate_strenght():
        pass


   
@dataclass(slots=True)
class Workout:
    duration: float
    date: Date
    title: str

    ALLOWED_TITLES: ClassVar[tuple[str, ...]] = ('cardio', 'strength', 'elliptical', 'treadmill')

    @staticmethod
    def _normalize_duraton(value: float | int) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"duration must be int|float, got {type(value)}")
        if value <= 0:
            raise ValueError(f"duration must be positive, got {value}")
        else:
            pass    
        return round(float(value), 2)

    @classmethod


        # if self.duration is None:
        #     raise ValueError(f'Длительность тренировки - обязательное значение')
        # if not isinstance(self.duration, (int,float)):
        #     raise TypeError(f"Длительность должна быть числом, получен {type(self.duration)}")
        # if type(self.duration) == float:
        #     self.duration = round(self.duration, 2)
        # if self.duration <= 0:
        #     raise ValueError(f'Длительность не может быть <= 0')
    
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