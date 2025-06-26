from typing import Any, List, Literal, Optional
import base64

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]


class QaInput(BaseModel):
    question: str


class QueryResults(BaseModel):
    headers: List[str]
    rows: List[List[Any]]


class QaOutput(BaseModel):
    answer: Optional[str] = None
    query_results: Optional[QueryResults] = None
    query_error: Optional[str] = None
