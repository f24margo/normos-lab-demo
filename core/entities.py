from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Any, List, Optional

class NormEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class NormDecision(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    result: str
    verb: str
    modality: str
    trace: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
