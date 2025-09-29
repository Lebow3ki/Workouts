from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import ClassVar, Optional


@dataclass(slots=True)
class User:
    """
    Represents a user.

    Fields:
      - tg_id: Telegram ID (non-empty string).
      - created_at: timezone-aware datetime in UTC, set automatically.
      - age: years (optional, >= 0).
      - weight_kg: weight in kilograms (optional, > 0).
      - height_cm: height in centimeters (optional, > 0).
      - sex: optional, one of "male"|"female".
    """
    tg_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    sex: Optional[str] = None

    # class counter (optional, for debug/demo)
    count: ClassVar[int] = 0

    def __post_init__(self):
        # validate fields in order
        self._validate_tg_id()
        self._validate_optional_numbers()
        self._validate_sex()
        # increase class counter
        User.count += 1

    def _validate_tg_id(self) -> None:
        # 1) type
        if not isinstance(self.tg_id, str):
            raise TypeError(f"tg_id must be a str, got {type(self.tg_id).__name__}")
        # 2) normalize
        self.tg_id = self.tg_id.strip()
        # 3) required non-empty
        if self.tg_id == "":
            raise ValueError("tg_id must be a non-empty string")


    def _validate_optional_numbers(self) -> None:
        if self.age is not None:
            if not isinstance(self.age, int):
                raise TypeError("age must be int or None")
            if self.age < 0:
                raise ValueError("age must be >= 0")
        if self.weight_kg is not None:
            if not isinstance(self.weight_kg, (int, float)):
                raise TypeError("weight_kg must be a number or None")
            if self.weight_kg <= 0:
                raise ValueError("weight_kg must be > 0")
        if self.height_cm is not None:
            if not isinstance(self.height_cm, (int, float)):
                raise TypeError("height_cm must be a number or None")
            if self.height_cm <= 0:
                raise ValueError("height_cm must be > 0")

    def _validate_sex(self) -> None:
        if self.sex is None:
            return
        if not isinstance(self.sex, str):
            raise TypeError("sex must be a string or None")
        self.sex = self.sex.strip().lower()
        if self.sex not in {"male", "female"}:
            raise ValueError("sex must be 'male' or 'female' if provided")

Mario = User(tg_id="Mario", age=35, weight_kg=135.5, height_cm=178, sex='male')
print(Mario)

@dataclass(slots=True)
class Exercise:
    kind: str # strength, cardio
    title: str
    duration_min: float #must be > 0
    # must be for strength
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    sets: Optional[int] = None
    # class counter (optional, for debug/demo)
    count: ClassVar[int] = 0

    def __post_init__(self):
        self._validate_kind()
        self._validate_title()
        self._validate_duration_min()
        Exercise.count += 1

    def _validate_kind(self):
        if not isinstance(self.kind, str):
            raise TypeError(f"kind must be a str, got {type(self.kind).__name__}")
        self.kind = self.kind.strip().lower()
        if self.kind not in {"strength", "cardio"}:
            raise ValueError(f"kind must be 'strength', 'cardio'")
        else:
            if self.kind == "strength":
                # Check weight_kg
                if not isinstance(self.weight_kg, float):
                    if isinstance(self.weight_kg, int):
                        self.weight_kg = float(self.weight_kg)
                    else:
                        raise TypeError("weight_kg must be provided and must be a number")
                if self.weight_kg <= 0:
                    raise ValueError("weight_kg must be > 0")
                # Check reps
                if not isinstance(self.reps, int):
                        raise TypeError("reps must be provided and must be a int")
                if self.reps <= 0:
                    raise ValueError("reps must be > 0")
                # Check sets
                if not isinstance(self.sets, int):
                        raise TypeError("sets must be provided and must be a int")
                if self.sets <= 0:
                    raise ValueError("sets must be > 0") 
            elif self.kind == "cardio":
                if not self.weight_kg is None:
                    raise TypeError(f'Cardio cannot include weight_kg')
                if not self.reps is None:
                    raise TypeError(f'Cardio cannot include reps')
                if not self.sets is None:
                    raise TypeError(f'Cardio cannot include sets')

    def _validate_title(self) -> None:
        if not isinstance(self.title, str):
            raise TypeError(f"title must be a str, got {type(self.title).__name__}")
        self.title = self.title.strip().lower()
        if self.title == "":
            raise ValueError("title must be a non-empty string")

    def _validate_duration_min(self):
        if not isinstance(self.duration_min, float):
            if isinstance(self.duration_min, int):
                self.duration_min = float(self.duration_min)
            else:
                raise TypeError("duration must be provided and must be a number")
        if self.duration_min <= 0:
            raise ValueError("duration must be > 0")
    
    def to_dict(self):
        if self.kind == "strength":
            result = {'kind': self.kind, 'title': self.title, 'duration_min': self.duration_min, 'weight_kg': self.weight_kg, 'reps': self.reps, 'sets': self.sets}
        elif self.kind == "cardio":
            result = {'kind': self.kind, 'title': self.title, 'duration_min': self.duration_min}                    
        return result                   

workout = Exercise('strength', 'pull-ups', 40, 50, 10, 4)
print(workout.sets)

@dataclass
class WorkoutSession:
    id: str
    user_id: str
    title: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_min: Optional[float] = None
    exercises = []

    def __post_init__(self):
        self.start_timer()

    def start_timer(self):
        if isinstance(self.start_time, datetime):
            raise ValueError(f'Workout has already started')
        else:
            self.start_time = datetime.now(timezone.utc)
            return self.start_time

    def stop_timer(self):
        if not isinstance(self.start_time, datetime):
            raise ValueError("cannot stop once workout is not started")
        if not self.exercises:
            raise ValueError("cannot stop once workout exercises not set")
        self.end_time = datetime.now(timezone.utc)
        self.duration_minutes()
        return self.end_time

    def add_exercise(self, exercise: Exercise):
        if self.start_time:
            if self.end_time is None:
                self.exercises.append(exercise)
            else:
                if self.end_time:
                    raise ValueError("cannot add exercises if workout is already over")
        elif not self.start_time:
            raise ValueError("cannot add exercises if workout has not started")
        return self.exercises

    def is_open(self):
        if self.start_time:
            if self.end_time is None:
                return True
            else:
                return False
        else:
            raise ValueError("Session has not started")

    def duration_minutes(self):
        try:
            if self.is_open():
                now = datetime.now(timezone.utc)
                self.duration_min = round((now - self.start_time).total_seconds() / 60, 2)
                return self.duration_min
            else:
                self.duration_min = round((self.end_time - self.start_time).total_seconds() / 60, 2)
                return self.duration_min
        except ValueError:
            return float(0)

    def to_dict(self):
        if self.is_open():
            raise ValueError("Session has not ended")
        else:
            ex_dict = []
            for ex in self.exercises:
                ex_dict = ex_dict.append(ex.to_dict())
            result= { 
                'id': self.id,
                'user_id': self.user_id,
                'title': self.title,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'duration_min': self.duration_min,
                'exercises': ex_dict 
            }
        return result