"""
Tests for the financial data API routes
"""
import pytest
from httpx import AsyncClient
from fastapi import status
from datetime import date

# Import the app instance for async testing
from app.main import app


@pytest.mark.asyncio
async def test_create_financial_data(clear_db):
    """Test creating a financial data record via API"""
    # Create a simple record via API
    data = {
        "boolean_value": True,
        "term_sheet_status": "Yes",
        "numeric_value": 42.5,
        "date_value": "2025-04-10"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is True
    assert response_data["term_sheet_status"] == "Yes"
    assert response_data["numeric_value"] == 42.5
    assert response_data["date_value"] == "2025-04-10"
    assert "id" in response_data
    assert response_data["id"] is not None


@pytest.mark.asyncio
async def test_create_financial_data_with_composite_value(clear_db):
    """Test creating a financial data record with composite value via API"""
    # Create data with composite value
    data = {
        "boolean_value": True,
        "numeric_value": 50.0,
        "composite_value": {
            "type": "number",
            "value": 1000000
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is True
    assert response_data["numeric_value"] == 50.0
    assert response_data["composite_value"]["type"] == "number"
    assert response_data["composite_value"]["value"] == 1000000


@pytest.mark.asyncio
async def test_create_financial_data_with_greater_of_value(clear_db):
    """Test creating a financial data record with greater_of composite value via API"""
    # Create data with greater_of composite value
    data = {
        "boolean_value": False,
        "numeric_value": 75.0,
        "composite_value": {
            "type": "greater_of",
            "details": {
                "amount": 1000000,
                "percentage": 5.0,
                "metric": "EBITDA"
            }
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is False
    assert response_data["numeric_value"] == 75.0
    assert response_data["composite_value"]["type"] == "greater_of"
    assert response_data["composite_value"]["details"]["amount"] == 1000000
    assert response_data["composite_value"]["details"]["percentage"] == 5.0
    assert response_data["composite_value"]["details"]["metric"] == "EBITDA"


@pytest.mark.asyncio
async def test_create_financial_data_with_percentage_multiple(clear_db):
    """Test creating a financial data record with percentage_multiple via API"""
    # Create data with percentage multiple
    data = {
        "boolean_value": True,
        "numeric_value": 60.0,
        "percentage_multiple": {
            "type": "percentage",
            "value": 25.0
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is True
    assert response_data["numeric_value"] == 60.0
    assert response_data["percentage_multiple"]["type"] == "percentage"
    assert response_data["percentage_multiple"]["value"] == 25.0


@pytest.mark.asyncio
async def test_create_financial_data_with_names_list(clear_db):
    """Test creating a financial data record with names_list via API"""
    # Create data with names list
    names = ["John Smith", "Jane Doe", "Robert Johnson"]
    data = {
        "boolean_value": True,
        "numeric_value": 70.0,
        "names_list": {
            "type": "names_list",
            "names": names
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is True
    assert response_data["numeric_value"] == 70.0
    assert response_data["names_list"]["type"] == "names_list"
    assert response_data["names_list"]["names"] == names


@pytest.mark.asyncio
async def test_create_financial_data_with_financial_ratio(clear_db):
    """Test creating a financial data record with financial_ratio via API"""
    # Create data with financial ratio
    data = {
        "boolean_value": False,
        "numeric_value": 80.0,
        "financial_ratio": {
            "type": "total_net",
            "ratio": 3.5
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is False
    assert response_data["numeric_value"] == 80.0
    assert response_data["financial_ratio"]["type"] == "total_net"
    assert response_data["financial_ratio"]["ratio"] == 3.5


@pytest.mark.asyncio
async def test_create_financial_data_with_percentage_condition(clear_db):
    """Test creating a financial data record with percentage_condition via API"""
    # Create data with percentage condition
    data = {
        "boolean_value": True,
        "numeric_value": 90.0,
        "percentage_condition": {
            "type": "with_leverage_test",
            "percentage": 15.0,
            "test": {
                "multiplier": 2.5,
                "metric": "EBITDA"
            }
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    
    # Check response data
    response_data = response.json()
    assert response_data["boolean_value"] is True
    assert response_data["numeric_value"] == 90.0
    assert response_data["percentage_condition"]["type"] == "with_leverage_test"
    assert response_data["percentage_condition"]["percentage"] == 15.0
    assert response_data["percentage_condition"]["test"]["multiplier"] == 2.5
    assert response_data["percentage_condition"]["test"]["metric"] == "EBITDA"


@pytest.mark.asyncio
async def test_get_all_financial_data(clear_db, create_test_data):
    """Test getting all financial data records via API"""
    # First, create a test record
    test_record = await create_test_data
    
    # Now test the GET all endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/financial_data/")
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    # Check response data
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["id"] == test_record.id


@pytest.mark.asyncio
async def test_get_financial_data_by_id(clear_db, create_test_data):
    """Test getting a specific financial data record by ID via API"""
    # First, create a test record
    test_record = await create_test_data
    
    # Now test the GET by ID endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/financial_data/{test_record.id}")
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    # Check response data
    response_data = response.json()
    assert response_data["id"] == test_record.id
    assert response_data["boolean_value"] == test_record.boolean_value
    assert response_data["numeric_value"] == test_record.numeric_value


@pytest.mark.asyncio
async def test_get_financial_data_by_id_not_found(clear_db):
    """Test getting a non-existent financial data record by ID via API"""
    # Use a non-existent ID
    non_existent_id = 999
    
    # Test the GET by ID endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/financial_data/{non_existent_id}")
    
    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_financial_data(clear_db, create_test_data):
    """Test updating a financial data record via API"""
    # First, create a test record
    test_record = await create_test_data
    
    # Now test the PUT endpoint
    update_data = {
        "boolean_value": False,  # Changed from True
        "term_sheet_status": "No",  # Changed from Yes
        "numeric_value": 200.0,  # Changed from original value
        "date_value": "2025-04-11"  # Changed from original date
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/financial_data/{test_record.id}", json=update_data)
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    # Check response data
    response_data = response.json()
    assert response_data["id"] == test_record.id
    assert response_data["boolean_value"] is False
    assert response_data["term_sheet_status"] == "No"
    assert response_data["numeric_value"] == 200.0
    assert response_data["date_value"] == "2025-04-11"


@pytest.mark.asyncio
async def test_update_financial_data_not_found(clear_db):
    """Test updating a non-existent financial data record via API"""
    # Use a non-existent ID
    non_existent_id = 999
    
    # Test the PUT endpoint
    update_data = {
        "boolean_value": False,
        "numeric_value": 200.0
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/financial_data/{non_existent_id}", json=update_data)
    
    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_financial_data(clear_db, create_test_data):
    """Test deleting a financial data record via API"""
    # First, create a test record
    test_record = await create_test_data
    
    # Now test the DELETE endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/financial_data/{test_record.id}")
    
    # Verify response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the record is gone by trying to get it
    async with AsyncClient(app=app, base_url="http://test") as ac:
        verify_response = await ac.get(f"/financial_data/{test_record.id}")
    
    assert verify_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_financial_data_not_found(clear_db):
    """Test deleting a non-existent financial data record via API"""
    # Use a non-existent ID
    non_existent_id = 999
    
    # Test the DELETE endpoint
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/financial_data/{non_existent_id}")
    
    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_pagination_get_all_financial_data(clear_db):
    """Test pagination for getting all financial data records via API"""
    # Create multiple records
    from app.models.financial_data import FinancialData
    
    # Create 5 test records
    for i in range(5):
        await FinancialData.create(
            boolean_value=(i % 2 == 0),
            numeric_value=50.0 + i,
            date_value=date(2025, 4, 10 + i)
        )
    
    # Test pagination with limit=2, offset=1
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/financial_data/?limit=2&offset=1")
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    # Check response data
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 2  # Should return exactly 2 records


@pytest.mark.asyncio
async def test_create_financial_data_with_invalid_data(clear_db):
    """Test creating a financial data record with invalid data via API"""
    # Create data with invalid term sheet status
    data = {
        "boolean_value": True,
        "term_sheet_status": "Invalid",  # Invalid value
        "numeric_value": 42.5
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/financial_data/", json=data)
    
    # Verify response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_financial_data_with_complex_fields(clear_db, create_test_data):
    """Test updating complex fields in a financial data record via API"""
    # First, create a test record
    test_record = await create_test_data
    
    # Now test the PUT endpoint with updates to complex fields
    update_data = {
        "boolean_value": True,
        "numeric_value": 42.5,
        "composite_value": {
            "type": "number",  # Changed from greater_of
            "value": 2000000   # New value
        },
        "percentage_multiple": {
            "type": "percentage",
            "value": 30.0  # Changed from 25.0
        },
        "names_list": {
            "type": "names_list",
            "names": ["Updated Name 1", "Updated Name 2"]  # Changed names
        }
    }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/financial_data/{test_record.id}", json=update_data)
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    # Check response data
    response_data = response.json()
    assert response_data["id"] == test_record.id
    assert response_data["composite_value"]["type"] == "number"
    assert response_data["composite_value"]["value"] == 2000000
    assert response_data["percentage_multiple"]["value"] == 30.0
    assert response_data["names_list"]["names"] == ["Updated Name 1", "Updated Name 2"]
