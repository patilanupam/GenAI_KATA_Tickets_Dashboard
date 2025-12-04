"""
Data models for meeting minutes
This module defines Pydantic models for meeting minutes and related entities.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ActionItem(BaseModel):
    """Model for an action item from a meeting."""
    description: str = Field(..., description="Description of the action item")
    owner: Optional[str] = Field(default="Unassigned", description="Person responsible for the action")
    due_date: Optional[str] = Field(default=None, description="Due date for the action item")
    priority: str = Field(default="Medium", description="Priority level: High, Medium, or Low")
    status: str = Field(default="Open", description="Status of the action item")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Prepare Q4 financial report",
                "owner": "John Doe",
                "due_date": "2025-12-15",
                "priority": "High",
                "status": "Open"
            }
        }


class Decision(BaseModel):
    """Model for a decision made in a meeting."""
    decision: str = Field(..., description="The decision that was made")
    rationale: Optional[str] = Field(default=None, description="Reasoning behind the decision")
    owner: Optional[str] = Field(default=None, description="Person who made or is responsible for the decision")
    impact: Optional[str] = Field(default=None, description="Expected impact of the decision")

    class Config:
        json_schema_extra = {
            "example": {
                "decision": "Adopt microservices architecture for new product",
                "rationale": "Better scalability and maintainability",
                "owner": "Tech Lead",
                "impact": "Will require 3 months of refactoring"
            }
        }


class Risk(BaseModel):
    """Model for a risk identified in a meeting."""
    risk: str = Field(..., description="Description of the risk")
    impact: Optional[str] = Field(default=None, description="Potential impact if risk materializes")
    mitigation: Optional[str] = Field(default=None, description="Mitigation strategy")
    owner: Optional[str] = Field(default=None, description="Person responsible for managing the risk")
    severity: Optional[str] = Field(default="Medium", description="Severity level: High, Medium, or Low")

    class Config:
        json_schema_extra = {
            "example": {
                "risk": "Database migration might cause downtime",
                "impact": "Service unavailable for up to 2 hours",
                "mitigation": "Perform migration during off-peak hours with rollback plan",
                "owner": "DevOps Team",
                "severity": "High"
            }
        }


class SpeakerSpotlight(BaseModel):
    """Model for speaker analysis and highlights."""
    speaker: str = Field(..., description="Name of the speaker")
    speaking_time_estimate: Optional[str] = Field(default=None, description="Estimated speaking time")
    notable_points: List[str] = Field(default_factory=list, description="Key points mentioned by speaker")
    sentiment: Optional[str] = Field(default=None, description="Overall sentiment: Positive, Neutral, Negative")

    class Config:
        json_schema_extra = {
            "example": {
                "speaker": "Jane Smith",
                "speaking_time_estimate": "15%",
                "notable_points": [
                    "Proposed new marketing strategy",
                    "Raised concerns about budget allocation"
                ],
                "sentiment": "Neutral"
            }
        }


class Metadata(BaseModel):
    """Model for meeting metadata."""
    transcript_length_words: Optional[int] = Field(default=None, description="Number of words in transcript")
    detected_date: Optional[str] = Field(default=None, description="Detected meeting date from transcript")
    meeting_duration: Optional[str] = Field(default=None, description="Estimated meeting duration")
    confidence_notes: Optional[str] = Field(default=None, description="Notes about confidence in extraction")
    generated_at: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="When minutes were generated")

    class Config:
        json_schema_extra = {
            "example": {
                "transcript_length_words": 2500,
                "detected_date": "2025-12-04",
                "meeting_duration": "1 hour",
                "confidence_notes": "High confidence in extraction",
                "generated_at": "2025-12-04T10:30:00Z"
            }
        }


class MeetingMinutes(BaseModel):
    """Complete model for meeting minutes."""
    executive_summary: List[str] = Field(default_factory=list, description="Executive summary of the meeting")
    action_items: List[ActionItem] = Field(default_factory=list, description="List of action items")
    decisions: List[Decision] = Field(default_factory=list, description="List of decisions made")
    risks: List[Risk] = Field(default_factory=list, description="List of risks identified")
    speaker_spotlight: List[SpeakerSpotlight] = Field(default_factory=list, description="Speaker analysis")
    metadata: Optional[Metadata] = Field(default=None, description="Meeting metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "executive_summary": [
                    "Discussed Q4 product roadmap",
                    "Reviewed budget allocation for new features",
                    "Identified key risks in migration plan"
                ],
                "action_items": [
                    {
                        "description": "Prepare Q4 financial report",
                        "owner": "John Doe",
                        "due_date": "2025-12-15",
                        "priority": "High",
                        "status": "Open"
                    }
                ],
                "decisions": [
                    {
                        "decision": "Adopt microservices architecture",
                        "rationale": "Better scalability",
                        "owner": "Tech Lead"
                    }
                ],
                "risks": [],
                "speaker_spotlight": [],
                "metadata": {
                    "transcript_length_words": 2500,
                    "generated_at": "2025-12-04T10:30:00Z"
                }
            }
        }


class MinutesResponse(BaseModel):
    """API response model for meeting minutes."""
    minutes: MeetingMinutes = Field(..., description="The generated meeting minutes")
    llm_trace: Optional[Dict[str, Any]] = Field(default=None, description="LLM processing trace information")

    class Config:
        json_schema_extra = {
            "example": {
                "minutes": {
                    "executive_summary": ["Meeting summary point 1", "Meeting summary point 2"],
                    "action_items": [],
                    "decisions": [],
                    "risks": [],
                    "speaker_spotlight": [],
                    "metadata": {"transcript_length_words": 2500}
                },
                "llm_trace": {
                    "prompt": "System prompt used...",
                    "model": "llama2"
                }
            }
        }


# Legacy compatibility alias
MinutesModel = MeetingMinutes

 