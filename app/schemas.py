import re
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import validator, BaseModel

@dataclass
class Fund:
    code: str = None
    title: str = None
    last_price: float = None
    daily_return: float = None
    total_value_try: float = None
    last_1_month_return: float = None
    last_3_months_return: float = None
    last_6_months_return: float = None
    last_1_year_return: Optional[float] | None = None
