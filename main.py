from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import ClassVar, Optional, List, Dict, Any
import json
from pathlib import Path


# ──────────────────────────────
# ВСПОМОГАТЕЛЬНОЕ: ISO-время UTC
# ──────────────────────────────
def _iso_utc(dt: Optional[datetime]) -> Optional[str]:
    """Стандартизируем сериализацию времени: ISO-8601 в UTC с 'Z'."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")

# ──────────────────────────────
# ВСПОМОГАТЕЛЬНОЕ: Export to JSON
# ──────────────────────────────

# def _to_json(obj, filename: str = 'wrksdata'):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(obj, f, indent=2, ensure_ascii=False)

# ──────────────────────────────
# USER
# ──────────────────────────────
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
        self._validate_tg_id()
        self._validate_optional_numbers()
        self._validate_sex()
        User.count += 1

    def _validate_tg_id(self) -> None:
        if not isinstance(self.tg_id, str):
            raise TypeError(f"tg_id must be a str, got {type(self.tg_id).__name__}")
        self.tg_id = self.tg_id.strip()
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


# ──────────────────────────────
# EXERCISE
# ──────────────────────────────
@dataclass(slots=True)
class Exercise:
    kind: str          # "strength" | "cardio"
    title: str
    duration_min: float  # must be > 0
    # strength-only
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    sets: Optional[int] = None

    # class counter (optional)
    count: ClassVar[int] = 0

    def __post_init__(self):
        # CHANGED: был post_init
        self._validate_kind()
        self._validate_title()
        self._validate_duration_min()
        Exercise.count += 1

    def _validate_kind(self) -> None:
        if not isinstance(self.kind, str):
            raise TypeError(f"kind must be a str, got {type(self.kind)._name_}")
        self.kind = self.kind.strip().lower()
        if self.kind not in {"strength", "cardio"}:
            raise ValueError("kind must be 'strength' or 'cardio'")

        if self.kind == "strength":
            # weight_kg
            if self.weight_kg is None or not isinstance(self.weight_kg, (int, float)):
                raise TypeError("weight_kg must be provided and must be a number for strength")
            if float(self.weight_kg) <= 0:
                raise ValueError("weight_kg must be > 0 for strength")
            # reps
            if self.reps is None or not isinstance(self.reps, int):
                raise TypeError("reps must be provided and must be an int for strength")
            if self.reps <= 0:
                raise ValueError("reps must be > 0 for strength")
            # sets
            if self.sets is None or not isinstance(self.sets, int):
                raise TypeError("sets must be provided and must be an int for strength")
            if self.sets <= 0:
                raise ValueError("sets must be > 0 for strength")

        else:  # cardio
            # явные проверки is not None — запрещаем силовые поля у кардио
            if self.weight_kg is not None:
                raise TypeError("cardio cannot include weight_kg")
            if self.reps is not None:
                raise TypeError("cardio cannot include reps")
            if self.sets is not None:
                raise TypeError("cardio cannot include sets")

    def _validate_title(self) -> None:
        if not isinstance(self.title, str):
            raise TypeError(f"title must be a str, got {type(self.title)._name_}")
        self.title = self.title.strip()
        if self.title == "":
            raise ValueError("title must be a non-empty string")

    def _validate_duration_min(self) -> None:
        # допускаем int → приводим к float
        if not isinstance(self.duration_min, (int, float)):
            raise TypeError("duration_min must be a number")
        self.duration_min = float(self.duration_min)
        if self.duration_min <= 0:
            raise ValueError("duration_min must be > 0")

    def to_dict(self) -> Dict[str, Any]:
        # CHANGED: единый ключ duration_min, без опечаток
        base = {"kind": self.kind, "title": self.title, "duration_min": self.duration_min}
        if self.kind == "strength":
            base.update({"weight_kg": float(self.weight_kg), "reps": self.reps, "sets": self.sets})
        return base


# ──────────────────────────────
# WORKOUT SESSION
# ──────────────────────────────
@dataclass(slots=True)
class WorkoutSession:
    id: str
    user_id: str
    title: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_min: Optional[float] = None
    # У каждого экземпляра свой список 
    exercises: List[Exercise] = field(default_factory=list)

    def __post_init__(self):
        # Сессия создаётся «холодной», стартуем вручную.
        pass

    # ── жизненный цикл ──
    def start_timer(self) -> datetime:
        if self.start_time is not None:
            raise ValueError("workout has already started")
        self.start_time = datetime.now(timezone.utc)
        return self.start_time

    def stop_timer(self) -> float:
        if self.start_time is None:
            raise ValueError("cannot stop workout that has not started")
        if not self.exercises:
            raise ValueError("cannot stop workout without exercises")
        self.end_time = datetime.now(timezone.utc)
        self.duration_min = round((self.end_time - self.start_time).total_seconds() / 60, 2)
        return self.duration_min

    def is_open(self) -> bool:
        # не кидаем исключения; для вызова в любом состоянии
        return self.start_time is not None and self.end_time is None

    def add_exercise(self, exercise: Exercise) -> None:
        if not isinstance(exercise, Exercise):
            raise TypeError("exercise must be an Exercise instance")
        if self.start_time is None:
            raise ValueError("cannot add exercises if workout has not started")
        if self.end_time is not None:
            raise ValueError("cannot add exercises if workout is already over")
        self.exercises.append(exercise)

    def duration_minutes(self) -> float:
        # всегда возвращаем число, без исключений
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            now = datetime.now(timezone.utc)
            return round((now - self.start_time).total_seconds() / 60, 2)
        return round((self.end_time - self.start_time).total_seconds() / 60, 2)

    def to_dict(self) -> Dict[str, Any]:
        if self.is_open():
            raise ValueError("session is still open")
        # CHANGED: сериализуем datetime в ISO-строки и собираем упражнения в список словарей
        exercises_dicts = [ex.to_dict() for ex in self.exercises]
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "start_time": _iso_utc(self.start_time),
            "end_time": _iso_utc(self.end_time),
            "duration_min": self.duration_min if self.duration_min is not None else self.duration_minutes(),
            "exercises_count": len(self.exercises),
            "exercises": exercises_dicts,
        }
       
    def export_sessions_to_json(sessions: List[WorkoutSession], path: str | Path = 'exports/wrkts.json', *, pretty: bool = True) -> Path:
    # Сохранить список сессий в единый JSON-файл c шапкой метаданных.
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "version": "1.0",
            "exported_at": _iso_utc(datetime.now(timezone.utc)),
            "sessions": [s.to_dict() for s in sessions],
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2 if pretty else None)
        return path