import uuid
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SourceInfo(BaseModel):
    name: str
    url: str

class BaseEntity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_type: str
    name: str
    description: str
    url: str
    categories: List[str]
    source: SourceInfo
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Relationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: str
