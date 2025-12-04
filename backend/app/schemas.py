"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ActionItem(BaseModel):
    """Action item schema"""
    description: str
    owner: Optional[str] = "Unassigned"
    due_date: Optional[str] = None
    priority: str = "Medium"


class Decision(BaseModel):
    """Decision schema"""
    decision: str
    rationale: Optional[str] = None
    owner: Optional[str] = None


class Risk(BaseModel):
    """Risk schema"""
    risk: str
    impact: Optional[str] = None
    mitigation: Optional[str] = None
    owner: Optional[str] = None


class SpeakerSpotlight(BaseModel):
    """Speaker spotlight schema"""
    speaker: str
    speaking_time_estimate: Optional[str] = None
    notable_points: Optional[List[str]] = []


class Metadata(BaseModel):
    """Metadata schema"""
    transcript_length_words: Optional[int] = None
    detected_date: Optional[str] = None
    confidence_notes: Optional[str] = None


class MinutesResponse(BaseModel):
    """Complete meeting minutes response schema"""
    executive_summary: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    decisions: List[Decision] = Field(default_factory=list)
    risks: List[Risk] = Field(default_factory=list)
    speaker_spotlight: List[SpeakerSpotlight] = Field(default_factory=list)
    metadata: Optional[Metadata] = None

