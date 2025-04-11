"""
Test fixtures and configuration for pytest
"""
import os
import asyncio
import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer

from app.main import app, TORTOISE_ORM
from app.models.financial_data import FinancialData


# Override the event_loop fixture to use the same loop for all tests in the session
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    """Initialize test database and create schemas"""
    # Use an in-memory SQLite database for tests
    TEST_DB_URL = "sqlite://:memory:"
    
    # Configure Tortoise ORM with the test database
    test_config = TORTOISE_ORM.copy()
    test_config["connections"]["default"] = TEST_DB_URL
    
    # Initialize Tortoise ORM
    await Tortoise.init(config=test_config)
    
    # Create schema
    await Tortoise.generate_schemas(safe=True)
    
    # Return control
    yield
    
    # Cleanup
    await Tortoise.close_connections()


@pytest.fixture(scope="function")
def client():
    """Return a TestClient instance for FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def clear_db():
    """Clear all data between tests"""
    await FinancialData.all().delete()


@pytest.fixture
def sample_financial_data():
    """Return sample financial data for tests"""
    return {
        "boolean_value": True,
        "term_sheet_status": "Yes",
        "numeric_value": 42.5,
        "date_value": "2025-04-10",
        "composite_value": {
            "type": "greater_of",
            "details": {
                "amount": 1000000,
                "percentage": 5.0,
                "metric": "EBITDA"
            }
        },
        "percentage_multiple": {
            "type": "percentage",
            "value": 25.0
        },
        "names_list": {
            "type": "names_list",
            "names": ["John Smith", "Jane Doe", "Robert Johnson"]
        },
        "financial_ratio": {
            "type": "total_net",
            "ratio": 3.5
        },
        "percentage_condition": {
            "type": "with_leverage_test",
            "percentage": 15.0,
            "test": {
                "multiplier": 2.5,
                "metric": "EBITDA"
            }
        }
    }


@pytest.fixture
async def create_test_data(sample_financial_data):
    """Create a test record and return it"""
    # Create a record using the ORM directly (not through the API)
    record = await FinancialData.create(
        boolean_value=sample_financial_data["boolean_value"],
        term_sheet_status=sample_financial_data["term_sheet_status"],
        numeric_value=sample_financial_data["numeric_value"],
        date_value=sample_financial_data["date_value"],
        
        # Handle composite value
        composite_value_type=sample_financial_data["composite_value"]["type"],
        composite_value_data={"details": sample_financial_data["composite_value"]["details"]},
        
        # Handle percentage multiple
        percentage_multiple_type=sample_financial_data["percentage_multiple"]["type"],
        percentage_multiple_data={"value": sample_financial_data["percentage_multiple"]["value"]},
        
        # Handle names list
        names_list_type=sample_financial_data["names_list"]["type"],
        names_list_data={"names": sample_financial_data["names_list"]["names"]},
        
        # Handle financial ratio
        financial_ratio_type=sample_financial_data["financial_ratio"]["type"],
        financial_ratio_data={"ratio": sample_financial_data["financial_ratio"]["ratio"]},
        
        # Handle percentage condition
        percentage_condition_type=sample_financial_data["percentage_condition"]["type"],
        percentage_condition_data={
            "percentage": sample_financial_data["percentage_condition"]["percentage"],
            "test": sample_financial_data["percentage_condition"]["test"]
        }
    )
    
    return record
