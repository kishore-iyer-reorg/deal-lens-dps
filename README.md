# Financial Data API

A FastAPI-based API for managing complex financial data structures with Tortoise ORM and PostgreSQL.

## Features

- Complex data model for financial data with various composite value types
- FastAPI endpoints for CRUD operations
- Tortoise ORM for database interactions
- PostgreSQL as the database
- Aerich for database migrations
- Docker and Docker Compose for containerization

## Project Structure

```
financial_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API routes
│   └── models/
│       ├── __init__.py
│       ├── financial_data.py   # Tortoise ORM models
│       └── pydantic_models.py  # Pydantic models for API
│
├── migrations/                 # Aerich migrations
├── .env                        # Environment variables
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── init_db.py                  # Database initialization script
├── pyproject.toml              # Aerich configuration
└── requirements.txt            # Python dependencies
```

## Setup and Installation

### Using Docker Compose (Recommended)

1. Clone the repository
2. Start the services using Docker Compose:

```bash
docker-compose up -d
```

3. Initialize the database and create the first migration:

```bash
docker-compose exec web python init_db.py
```

4. The API will be available at http://localhost:8000

### Local Development Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Make sure PostgreSQL is running and update the DATABASE_URL in .env if needed
4. Initialize the database and create the first migration:

```bash
python init_db.py
```

5. Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

6. The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the auto-generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

### Creating a new migration

```bash
aerich migrate --name add_new_field
```

### Applying migrations

```bash
aerich upgrade
```

### Downgrading migrations

```bash
aerich downgrade
```

## Data Model

The API supports complex financial data structures with various composite value types:

- Basic values: booleans, numbers, dates, term sheet statuses
- Composite values:
  - Simple number or "Greater of" comparisons
  - Percentage multiples
  - Names lists
  - Financial ratios
  - Percentages with conditions

See the API documentation for detailed schema information and examples.

## License

MIT
