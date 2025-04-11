"""
Tests for Pydantic models
"""
import pytest
from datetime import date
from pydantic import ValidationError

from app.models.pydantic_models import (
    FinancialDataModel,
    TermSheetStatus,
    CompositeValueType,
    PercentageMultipleType,
    NamesListType,
    FinancialRatioType,
    PercentageConditionType,
    NumberValue,
    GreaterOfValue,
    NoMinimumValue,
    NoPikValue,
    GreaterOfModel,
    PercentageMultipleValue,
    NoCashRequirementValue,
    PercentageNotStatedValue,
    NamesListValue,
    NamesListNAValue,
    FirstLienRatioValue,
    SeniorSecuredRatioValue,
    SecuredRatioValue,
    TotalNetRatioValue,
    FixedChargeRatioValue,
    InterestCoverageRatioValue,
    NoCovenantValue,
    RatioNotStatedValue,
    PercentageWithLeverageTestValue,
    PercentageNoLeverageTestValue,
    BasketNoComponentValue,
    NoBasketValue,
    PercentageConditionNotStatedValue,
    LeverageTestModel
)


def test_basic_financial_data_model():
    """Test basic FinancialDataModel with simple fields"""
    data = {
        "boolean_value": True,
        "term_sheet_status": "Yes",
        "numeric_value": 100.0,
        "date_value": "2025-04-10"
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.term_sheet_status == TermSheetStatus.YES
    assert model.numeric_value == 100.0
    assert model.date_value == date(2025, 4, 10)


def test_number_composite_value():
    """Test NumberValue composite type"""
    data = {
        "type": "number",
        "value": 1000000
    }
    
    model = NumberValue(**data)
    
    assert model.type == CompositeValueType.NUMBER
    assert model.value == 1000000


def test_greater_of_composite_value():
    """Test GreaterOfValue composite type"""
    greater_of_details = {
        "amount": 1000000,
        "percentage": 5.0,
        "metric": "EBITDA"
    }
    
    data = {
        "type": "greater_of",
        "details": greater_of_details
    }
    
    model = GreaterOfValue(**data)
    
    assert model.type == CompositeValueType.GREATER_OF
    assert model.details.amount == 1000000
    assert model.details.percentage == 5.0
    assert model.details.metric == "EBITDA"


def test_financial_data_with_composite_value():
    """Test FinancialDataModel with composite value"""
    data = {
        "boolean_value": True,
        "term_sheet_status": "Yes",
        "numeric_value": 100.0,
        "date_value": "2025-04-10",
        "composite_value": {
            "type": "number",
            "value": 1000000
        }
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.composite_value.type == CompositeValueType.NUMBER
    assert model.composite_value.value == 1000000


def test_financial_data_with_percentage_multiple():
    """Test FinancialDataModel with percentage multiple"""
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "percentage_multiple": {
            "type": "percentage",
            "value": 25.0
        }
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.percentage_multiple.type == PercentageMultipleType.PERCENTAGE
    assert model.percentage_multiple.value == 25.0


def test_financial_data_with_names_list():
    """Test FinancialDataModel with names list"""
    names = ["John Smith", "Jane Doe", "Robert Johnson"]
    
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "names_list": {
            "type": "names_list",
            "names": names
        }
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.names_list.type == NamesListType.NAMES_LIST
    assert model.names_list.names == names


def test_financial_data_with_financial_ratio():
    """Test FinancialDataModel with financial ratio"""
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "financial_ratio": {
            "type": "total_net",
            "ratio": 3.5
        }
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.financial_ratio.type == FinancialRatioType.TOTAL_NET
    assert model.financial_ratio.ratio == 3.5


def test_financial_data_with_percentage_condition():
    """Test FinancialDataModel with percentage condition"""
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "percentage_condition": {
            "type": "with_leverage_test",
            "percentage": 15.0,
            "test": {
                "multiplier": 2.5,
                "metric": "EBITDA"
            }
        }
    }
    
    model = FinancialDataModel(**data)
    
    assert model.boolean_value is True
    assert model.percentage_condition.type == PercentageConditionType.WITH_LEVERAGE_TEST
    assert model.percentage_condition.percentage == 15.0
    assert model.percentage_condition.test.multiplier == 2.5
    assert model.percentage_condition.test.metric == "EBITDA"


def test_complete_financial_data_model():
    """Test FinancialDataModel with all possible fields"""
    data = {
        "id": 1,
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
        },
        "created_at": "2025-04-10T10:00:00",
        "updated_at": "2025-04-10T10:00:00"
    }
    
    model = FinancialDataModel(**data)
    
    # Check all fields
    assert model.id == 1
    assert model.boolean_value is True
    assert model.term_sheet_status == TermSheetStatus.YES
    assert model.numeric_value == 42.5
    assert model.date_value == date(2025, 4, 10)
    
    # Check composite value
    assert model.composite_value.type == CompositeValueType.GREATER_OF
    assert model.composite_value.details.amount == 1000000
    assert model.composite_value.details.percentage == 5.0
    assert model.composite_value.details.metric == "EBITDA"
    
    # Check percentage multiple
    assert model.percentage_multiple.type == PercentageMultipleType.PERCENTAGE
    assert model.percentage_multiple.value == 25.0
    
    # Check names list
    assert model.names_list.type == NamesListType.NAMES_LIST
    assert model.names_list.names == ["John Smith", "Jane Doe", "Robert Johnson"]
    
    # Check financial ratio
    assert model.financial_ratio.type == FinancialRatioType.TOTAL_NET
    assert model.financial_ratio.ratio == 3.5
    
    # Check percentage condition
    assert model.percentage_condition.type == PercentageConditionType.WITH_LEVERAGE_TEST
    assert model.percentage_condition.percentage == 15.0
    assert model.percentage_condition.test.multiplier == 2.5
    assert model.percentage_condition.test.metric == "EBITDA"
    
    # Check timestamps
    assert model.created_at == "2025-04-10T10:00:00"
    assert model.updated_at == "2025-04-10T10:00:00"


def test_invalid_term_sheet_status():
    """Test validation error with invalid term sheet status"""
    data = {
        "boolean_value": True,
        "term_sheet_status": "Invalid",  # Invalid value
        "numeric_value": 100.0
    }
    
    with pytest.raises(ValidationError):
        FinancialDataModel(**data)


def test_invalid_composite_value_type():
    """Test validation error with invalid composite value type"""
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "composite_value": {
            "type": "invalid_type",  # Invalid type
            "value": 1000000
        }
    }
    
    with pytest.raises(ValidationError):
        FinancialDataModel(**data)


def test_missing_required_field_in_composite():
    """Test validation error when required field is missing in composite value"""
    data = {
        "boolean_value": True,
        "numeric_value": 100.0,
        "composite_value": {
            "type": "number"
            # Missing "value" field
        }
    }
    
    with pytest.raises(ValidationError):
        FinancialDataModel(**data)
