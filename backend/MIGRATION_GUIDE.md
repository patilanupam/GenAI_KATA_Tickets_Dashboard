# Backend Restructuring Migration Guide

## Overview
The backend directory has been successfully restructured according to the new specifications.

## New Directory Structure

```
backend/
├─ app/
│  ├─ __init__.py                # Package initialization
│  ├─ main.py                    # FastAPI application entry point
│  ├─ config.py                  # Application configuration settings
│  ├─ langgraph_agent.py         # LangGraph-based minutes generator
│  ├─ schemas.py                 # Pydantic schemas for API
│  └─ services/
│     ├─ __init__.py             # Services package initialization
│     ├─ storage.py              # Optional storage utilities (file caching, S3, etc.)
│     ├─ text_cleaner.py         # Transcript text cleaning utilities
│     └─ speaker_parser.py       # Speaker parsing and segmentation
├─ Dockerfile                    # Docker configuration
├─ requirements.txt              # Python dependencies
├─ agent/                        # OLD - Can be removed
│  ├─ langgraph_agent.py
│  └─ prompts.py
├─ models/                       # OLD - Can be removed
│  └─ minutes.py
├─ utils/                        # OLD - Can be removed
│  └─ transcript_parser.py
└─ main.py                       # OLD - Can be removed
```

## File Mappings

### Moved Files
- `backend/main.py` → `backend/app/main.py`
- `backend/agent/langgraph_agent.py` → `backend/app/langgraph_agent.py`

### New Files Created
- `backend/app/__init__.py` - Package initialization
- `backend/app/config.py` - Configuration settings (extracted from main.py)
- `backend/app/schemas.py` - Pydantic models for API requests/responses
- `backend/app/services/__init__.py` - Services package initialization
- `backend/app/services/text_cleaner.py` - Text cleaning utilities
- `backend/app/services/speaker_parser.py` - Speaker parsing logic
- `backend/app/services/storage.py` - Optional storage service

### Files to be Deprecated
- `backend/main.py` (replaced by `backend/app/main.py`)
- `backend/agent/langgraph_agent.py` (moved to `backend/app/langgraph_agent.py`)
- `backend/agent/prompts.py` (integrated into langgraph_agent.py)
- `backend/models/minutes.py` (replaced by `backend/app/schemas.py`)
- `backend/utils/transcript_parser.py` (split into services)

## Key Changes

### 1. Configuration Management
- Created `config.py` with `Settings` class using pydantic-settings
- Centralized all configuration values (Ollama settings, API prefix, file size limits, etc.)

### 2. Schema Definitions
- Created comprehensive Pydantic schemas in `schemas.py`:
  - `ActionItem`
  - `Decision`
  - `Risk`
  - `SpeakerSpotlight`
  - `Metadata`
  - `MinutesResponse`

### 3. Service Layer
- **text_cleaner.py**: Handles transcript text normalization and cleaning
- **speaker_parser.py**: Parses transcript into speaker segments
- **storage.py**: Optional service for file caching and storage operations

### 4. Import Path Updates
All imports now use relative imports within the `app` package:
```python
from .config import settings
from .langgraph_agent import generate_minutes
from .schemas import MinutesResponse
from .services.text_cleaner import clean_transcript
from .services.speaker_parser import parse_speakers
```

## Next Steps

### 1. Update requirements.txt
Ensure all necessary dependencies are included:
```
fastapi
uvicorn[standard]
pydantic
pydantic-settings
httpx
langgraph
python-multipart
```

### 2. Update Dockerfile
Update the Dockerfile to reference the new structure:
```dockerfile
# Example update needed
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Remove Old Files (After Testing)
Once you've verified the new structure works:
```bash
rm backend/main.py
rm -rf backend/agent/
rm -rf backend/models/
rm -rf backend/utils/
```

### 4. Update Documentation
Update any documentation that references the old file structure.

### 5. Test the Application
Run the application to ensure all imports and functionality work correctly:
```bash
cd backend
uvicorn app.main:app --reload
```

## Benefits of New Structure

1. **Better Organization**: Clear separation between configuration, schemas, services, and application logic
2. **Scalability**: Easy to add new services without cluttering the main directory
3. **Maintainability**: Related code is grouped together logically
4. **Testing**: Services can be tested independently
5. **Standards Compliance**: Follows Python package best practices with __init__.py files

## Notes

- All new files follow Python best practices with proper docstrings
- Type hints are used throughout for better IDE support
- The structure is now more aligned with FastAPI best practices
- Services are modular and can be easily extended or replaced

