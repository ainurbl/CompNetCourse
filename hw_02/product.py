from typing import Optional

from pydantic import BaseModel


class TProduct(BaseModel):
    name: Optional[str]
    description: Optional[str]
