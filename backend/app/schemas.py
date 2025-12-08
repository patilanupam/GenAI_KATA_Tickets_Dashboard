"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum


class PriorityLevel(str, Enum):
    """Priority levels for action items"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class StatusLevel(str, Enum):
    """Status levels for action items"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    BLOCKED = "Blocked"


class ImpactLevel(str, Enum):
    """Impact levels for risks"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ActionItem(BaseModel):
    """Action item schema with validation"""
    description: str = Field(..., min_length=5, description="Clear description of the action")
    owner: str = Field(default="Unassigned", description="Person responsible for the action")
    due_date: Optional[str] = Field(None, description="Due date in YYYY-MM-DD format or relative (e.g., 'Next Monday')")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM, description="Priority level")
    status: StatusLevel = Field(default=StatusLevel.PENDING, description="Current status")

    @validator('description')
    def description_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Description cannot be empty')
        return v.strip()


class Decision(BaseModel):
    """Decision schema with enhanced tracking"""
    decision: str = Field(..., min_length=10, description="The decision that was made")
    rationale: Optional[str] = Field(None, description="Reason behind the decision")
    owner: Optional[str] = Field(None, description="Who made or is responsible for this decision")
    context: Optional[str] = Field(None, description="Context or background for the decision")


class Risk(BaseModel):
    """Risk/issue schema with impact tracking"""
    risk: str = Field(..., min_length=10, description="Description of the risk or issue")
    impact: ImpactLevel = Field(default=ImpactLevel.MEDIUM, description="Potential impact level")
    mitigation: Optional[str] = Field(None, description="Proposed mitigation strategy")
    owner: Optional[str] = Field(None, description="Person responsible for addressing this risk")


class SpeakerInfo(BaseModel):
    """Enhanced speaker information"""
    speaker: str = Field(..., description="Speaker name")
    role: Optional[str] = Field(None, description="Inferred role (e.g., PM, Developer, QA)")
    contribution_count: int = Field(default=0, description="Number of contributions")
    key_points: List[str] = Field(default_factory=list, description="Key points raised by speaker")


class Warning(BaseModel):
    """Warning for missing or ambiguous data"""
    type: str = Field(..., description="Type of warning (e.g., 'missing_owner', 'ambiguous_date')")
    message: str = Field(..., description="Human-readable warning message")
    context: Optional[str] = Field(None, description="Additional context about the warning")


class Metadata(BaseModel):
    """Enhanced metadata with processing info"""
    transcript_length_words: int = Field(default=0, description="Word count of transcript")
    transcript_length_chars: int = Field(default=0, description="Character count of transcript")
    speaker_count: int = Field(default=0, description="Number of unique speakers")
    processing_method: str = Field(default="llm", description="Processing method used (llm or fallback)")
    detected_dates: List[str] = Field(default_factory=list, description="All dates mentioned in transcript")
    confidence_score: Optional[str] = Field(None, description="Overall confidence in extraction quality")


class MinutesResponse(BaseModel):
    """Complete meeting minutes response with validation"""
    summary: List[str] = Field(
        default_factory=list,
        alias="executive_summary",
        description="Executive summary as bullet points"
    )
    actions: List[ActionItem] = Field(
        default_factory=list,
        alias="action_items",
        description="Extracted action items with owners and due dates"
    )
    decisions: List[Decision] = Field(
        default_factory=list,
        description="Key decisions made during the meeting"
    )
    risks: List[Risk] = Field(
        default_factory=list,
        description="Identified risks and issues"
    )
    speakers: List[SpeakerInfo] = Field(
        default_factory=list,
        alias="speaker_spotlight",
        description="Information about meeting participants"
    )
    warnings: List[Warning] = Field(
        default_factory=list,
        description="Warnings about missing or ambiguous data"
    )
    metadata: Metadata = Field(
        default_factory=Metadata,
        description="Processing metadata and statistics"
    )

    class Config:
        populate_by_name = True
        use_enum_values = True

