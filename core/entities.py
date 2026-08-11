from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Any, List, Optional

class TraceStep(BaseModel):
    label: str
    matched_verb: Optional[str] = None
    modality: Optional[str] = None
    step_type: Optional[str] = None  # init | verb_match | computation | oov | coverage

class NormEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class NormDecision(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_event_id: Optional[UUID] = None
    result: str
    verb: Optional[str] = None
    modality: Optional[str] = None
    trace: List[TraceStep] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
