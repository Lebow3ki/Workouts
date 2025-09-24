from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import ClassVar, Optional, Literal


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
    sex: Optional[Literal["male", "female"]] = None

    # class counter (optional, for debug/demo)
    count: ClassVar[int] = 0

    def _post_init_(self):
        # validate fields in order
        self._validate_tg_id()
        self._validate_optional_numbers()
        self._validate_sex()
        # increase class counter
        User.count += 1

    def _validate_tg_id(self) -> None:
        # 1) type
        if not isinstance(self.tg_id, str):
            raise TypeError(f"tg_id must be a str, got {type(self.tg_id)._name_}")
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
            raise ValueError("sex must be 'male' or 'female' if provided")
        
Mario = User(tg_id='mario', age=35, weight_kg=103.5, height_cm=178, sex='male')
print(Mario.created_at)
Luigi = User(tg_id='', age=35, weight_kg=103.5, height_cm=178, sex='mal')
print(Luigi)
print(User.count)