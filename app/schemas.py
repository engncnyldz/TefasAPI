from typing import Optional, Union
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
    last_1_year_return: float= None

    @validator("last_price", "daily_return", "total_value_try", "last_1_month_return", "last_3_months_return", "last_6_months_return", "last_1_year_return", pre=True)
    def validate_float_fields(cls, v):
        try:
            return float(v)
        except:
            return None
        
        
