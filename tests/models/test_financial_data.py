"""
Tests for FinancialData model
"""
import pytest
from datetime import date

from app.models.financial_data import (
    FinancialData, 
    TermSheetStatus, 
    CompositeValueType,
    PercentageMultipleType,
    NamesListType,
    FinancialRatioType,
    PercentageConditionType
)


@pytest.mark.asyncio
async def test_create_financial_data():
    """Test creating a financial data record"""
    # Create a simple record
    record = await FinancialData.create(
        boolean_value=True,
        term_sheet_status=TermSheetStatus.YES,
        numeric_value=100.0,
        date_value=date(2025, 4, 10)
    )
    
    # Verify it was created
    assert record.id is not None
    assert record.boolean_value is True
    assert record.term_sheet_status == TermSheetStatus.YES
    assert record.numeric_value == 100.0
    assert record.date_value == date(2025, 4, 10)


@pytest.mark.asyncio
async def test_create_with_composite_value():
    """Test creating a record with a composite value"""
    # Create a record with composite value
    record = await FinancialData.create(
        boolean_value=True,
        numeric_value=50.0,
        composite_value_type=CompositeValueType.NUMBER,
        composite_value_data={"value": 1000000}
    )
    
    # Verify composite value
    assert record.composite_value_type == CompositeValueType.NUMBER
    assert record.composite_value_data == {"value": 1000000}
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["composite_value"]["type"] == "number"
    assert record_dict["composite_value"]["value"] == 1000000


@pytest.mark.asyncio
async def test_create_with_greater_of_value():
    """Test creating a record with greater_of composite value"""
    # Create a record with greater_of composite value
    greater_of_data = {
        "details": {
            "amount": 1000000,
            "percentage": 5.0,
            "metric": "EBITDA"
        }
    }
    
    record = await FinancialData.create(
        boolean_value=False,
        numeric_value=75.0,
        composite_value_type=CompositeValueType.GREATER_OF,
        composite_value_data=greater_of_data
    )
    
    # Verify composite value
    assert record.composite_value_type == CompositeValueType.GREATER_OF
    assert record.composite_value_data == greater_of_data
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["composite_value"]["type"] == "greater_of"
    assert record_dict["composite_value"]["details"] == greater_of_data["details"]


@pytest.mark.asyncio
async def test_create_with_percentage_multiple():
    """Test creating a record with percentage_multiple composite value"""
    # Create a record with percentage multiple
    record = await FinancialData.create(
        boolean_value=True,
        numeric_value=60.0,
        percentage_multiple_type=PercentageMultipleType.PERCENTAGE,
        percentage_multiple_data={"value": 25.0}
    )
    
    # Verify percentage multiple
    assert record.percentage_multiple_type == PercentageMultipleType.PERCENTAGE
    assert record.percentage_multiple_data == {"value": 25.0}
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["percentage_multiple"]["type"] == "percentage"
    assert record_dict["percentage_multiple"]["value"] == 25.0


@pytest.mark.asyncio
async def test_create_with_names_list():
    """Test creating a record with names_list composite value"""
    names = ["John Smith", "Jane Doe", "Robert Johnson"]
    
    # Create a record with names list
    record = await FinancialData.create(
        boolean_value=True,
        numeric_value=70.0,
        names_list_type=NamesListType.NAMES_LIST,
        names_list_data={"names": names}
    )
    
    # Verify names list
    assert record.names_list_type == NamesListType.NAMES_LIST
    assert record.names_list_data == {"names": names}
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["names_list"]["type"] == "names_list"
    assert record_dict["names_list"]["names"] == names


@pytest.mark.asyncio
async def test_create_with_financial_ratio():
    """Test creating a record with financial_ratio composite value"""
    # Create a record with financial ratio
    record = await FinancialData.create(
        boolean_value=False,
        numeric_value=80.0,
        financial_ratio_type=FinancialRatioType.TOTAL_NET,
        financial_ratio_data={"ratio": 3.5}
    )
    
    # Verify financial ratio
    assert record.financial_ratio_type == FinancialRatioType.TOTAL_NET
    assert record.financial_ratio_data == {"ratio": 3.5}
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["financial_ratio"]["type"] == "total_net"
    assert record_dict["financial_ratio"]["ratio"] == 3.5


@pytest.mark.asyncio
async def test_create_with_percentage_condition():
    """Test creating a record with percentage_condition composite value"""
    condition_data = {
        "percentage": 15.0,
        "test": {
            "multiplier": 2.5,
            "metric": "EBITDA"
        }
    }
    
    # Create a record with percentage condition
    record = await FinancialData.create(
        boolean_value=True,
        numeric_value=90.0,
        percentage_condition_type=PercentageConditionType.WITH_LEVERAGE_TEST,
        percentage_condition_data=condition_data
    )
    
    # Verify percentage condition
    assert record.percentage_condition_type == PercentageConditionType.WITH_LEVERAGE_TEST
    assert record.percentage_condition_data == condition_data
    
    # Test dictionary conversion
    record_dict = record.to_dict()
    assert record_dict["percentage_condition"]["type"] == "with_leverage_test"
    assert record_dict["percentage_condition"]["percentage"] == 15.0
    assert record_dict["percentage_condition"]["test"] == condition_data["test"]


@pytest.mark.asyncio
async def test_delete_financial_data():
    """Test deleting a financial data record"""
    # Create a record
    record = await FinancialData.create(
        boolean_value=True,
        term_sheet_status=TermSheetStatus.YES,
        numeric_value=100.0,
        date_value=date(2025, 4, 10)
    )
    
    record_id = record.id
    
    # Delete the record
    await record.delete()
    
    # Verify it's gone
    deleted_record = await FinancialData.get_or_none(id=record_id)
    assert deleted_record is None


@pytest.mark.asyncio
async def test_update_financial_data():
    """Test updating a financial data record"""
    # Create a record
    record = await FinancialData.create(
        boolean_value=True,
        term_sheet_status=TermSheetStatus.YES,
        numeric_value=100.0,
        date_value=date(2025, 4, 10)
    )
    
    record_id = record.id
    
    # Update the record
    record.boolean_value = False
    record.term_sheet_status = TermSheetStatus.NO
    record.numeric_value = 200.0
    record.date_value = date(2025, 4, 11)
    await record.save()
    
    # Fetch the updated record
    updated_record = await FinancialData.get(id=record_id)
    
    # Verify updates
    assert updated_record.boolean_value is False
    assert updated_record.term_sheet_status == TermSheetStatus.NO
    assert updated_record.numeric_value == 200.0
    assert updated_record.date_value == date(2025, 4, 11)
