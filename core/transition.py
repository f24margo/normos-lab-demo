from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Any, List, Optional

class NormTransition(BaseModel):
    """Атомарная единица нормативной динамики (глава 5 монографии)"""
    
    id: UUID = Field(default_factory=uuid4)
    verb_id: str
    base_form: str
    modality: str
    transition_type: str
    
    from_state: str
    to_state: str
    
    agent: str
    object: Optional[str] = None
    context: Dict[str, Any]
    
    consequences: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    def describe(self) -> str:
        """Человекочитаемое описание перехода"""
        return f"{self.agent} {self.modality} {self.base_form} → {self.to_state}"
    
    def is_valid(self) -> bool:
        """Простая проверка целостности"""
        return bool(self.from_state and self.to_state and self.agent)
