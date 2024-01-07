from typing import List, Optional
from pydantic import BaseModel


class LoadDataFrame(BaseModel):
    file_paths: List[str]


class ChangeColumnNames(BaseModel):
    from_col_names: List[str]
    to_col_names: List[str]


class AltairPlot(BaseModel):
    data: str
    x: Optional[str]
    y: Optional[str]
    color: Optional[str]
    # size: Optional[int]


class ScatterPlot(AltairPlot):
    x: str
    y: str


class LinePlot(AltairPlot):
    x: str
    y: str


class BubblePlot(AltairPlot):
    x: str
    y: str


class AreaPlot(AltairPlot):
    x: str
    y: str
    func: str
