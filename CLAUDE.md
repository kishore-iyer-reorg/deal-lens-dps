# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands
- Start services: `docker-compose up -d`
- Initialize DB: `docker-compose exec web python init_db.py`
- Local development: `uvicorn app.main:app --reload`
- Create migration: `aerich migrate --name migration_name`
- Apply migrations: `aerich upgrade`
- Downgrade migrations: `aerich downgrade`

## Code Style Guidelines
- Imports: Group standard library, third-party, and local imports in that order
- Type annotations: Use Python type hints (Optional, Union, List, Dict, etc.)
- Error handling: Use explicit HTTP exceptions with status codes for API errors
- Naming: 
  - Snake_case for variables, functions, methods
  - PascalCase for classes and Pydantic models
  - Use Enum classes for predefined options
- Pydantic: Use BaseModel for data validation and JSON schema generation
- Database: Use Tortoise ORM models with appropriate field types
- Documentation: Use docstrings for functions/endpoints and detailed API examples
- Error handling: Validate input data with Pydantic, use try/except for DB operations