from typing import List
from pydantic import BaseModel


class DataFrame(BaseModel):
    file_paths: List[str]
