from pydantic import BaseModel, Field
from typing import Optional, Union, Literal, List
from enum import Enum
from datetime import date


class TermSheetStatus(str, Enum):
    YES = "Yes"
    PARTIAL = "Partial"
    NO = "No"
    NA = "N/A"
    NOT_STATED = "Not stated in Term Sheet"


# Original composite value models
class GreaterOfModel(BaseModel):
    """Model for 'Greater of [Amount] and X% of [metric]' type"""
    amount: float = Field(..., description="The fixed amount value")
    percentage: float = Field(..., description="The percentage value (e.g., 5.0 for 5%)")
    metric: str = Field(..., description="The metric to which the percentage applies")


class CompositeValueType(str, Enum):
    """Type discriminator for the composite value"""
    NUMBER = "number"
    GREATER_OF = "greater_of"
    NO_MINIMUM = "no_minimum"
    NO_PIK = "no_pik"


class NumberValue(BaseModel):
    """Container for simple numeric values"""
    type: Literal[CompositeValueType.NUMBER] = CompositeValueType.NUMBER
    value: float


class GreaterOfValue(BaseModel):
    """Container for 'Greater of' complex values"""
    type: Literal[CompositeValueType.GREATER_OF] = CompositeValueType.GREATER_OF
    details: GreaterOfModel


class NoMinimumValue(BaseModel):
    """Container for 'No minimum cash balance requirement' option"""
    type: Literal[CompositeValueType.NO_MINIMUM] = CompositeValueType.NO_MINIMUM


class NoPikValue(BaseModel):
    """Container for 'N/A, no PIK toggle applies' option"""
    type: Literal[CompositeValueType.NO_PIK] = CompositeValueType.NO_PIK


# Composite member 1: Percentage Multiple or No Requirement
class PercentageMultipleType(str, Enum):
    """Type discriminator for percentage multiple composite"""
    PERCENTAGE = "percentage"
    NO_CASH_REQUIREMENT = "no_cash_requirement"
    NOT_STATED = "not_stated"


class PercentageMultipleValue(BaseModel):
    """Container for percentage multiple value"""
    type: Literal[PercentageMultipleType.PERCENTAGE] = PercentageMultipleType.PERCENTAGE
    value: float = Field(..., description="The percentage multiple value (e.g., 5.0 for 5%)")


class NoCashRequirementValue(BaseModel):
    """Container for 'No cash consideration requirement' option"""
    type: Literal[PercentageMultipleType.NO_CASH_REQUIREMENT] = PercentageMultipleType.NO_CASH_REQUIREMENT


class PercentageNotStatedValue(BaseModel):
    """Container for 'Not stated in Term Sheet' option"""
    type: Literal[PercentageMultipleType.NOT_STATED] = PercentageMultipleType.NOT_STATED


# Composite member 2: Names List or N/A
class NamesListType(str, Enum):
    """Type discriminator for names list composite"""
    NAMES_LIST = "names_list"
    NA = "na"


class NamesListValue(BaseModel):
    """Container for list of names"""
    type: Literal[NamesListType.NAMES_LIST] = NamesListType.NAMES_LIST
    names: List[str] = Field(..., description="List of all names")


class NamesListNAValue(BaseModel):
    """Container for 'N/A' option for names list"""
    type: Literal[NamesListType.NA] = NamesListType.NA


# Composite member 3: Financial Ratio Types
class FinancialRatioType(str, Enum):
    """Type discriminator for financial ratio composite"""
    FIRST_LIEN = "first_lien"
    SENIOR_SECURED = "senior_secured"
    SECURED = "secured"
    TOTAL_NET = "total_net"
    FIXED_CHARGE = "fixed_charge"
    INTEREST_COVERAGE = "interest_coverage"
    NO_COVENANT = "no_covenant"
    NOT_STATED = "not_stated"


class FirstLienRatioValue(BaseModel):
    """First Lien Net Leverage Ratio"""
    type: Literal[FinancialRatioType.FIRST_LIEN] = FinancialRatioType.FIRST_LIEN
    ratio: float = Field(..., description="The ratio multiplier")


class SeniorSecuredRatioValue(BaseModel):
    """Senior Secured Net Leverage Ratio"""
    type: Literal[FinancialRatioType.SENIOR_SECURED] = FinancialRatioType.SENIOR_SECURED
    ratio: float = Field(..., description="The ratio multiplier")


class SecuredRatioValue(BaseModel):
    """Secured Net Leverage Ratio"""
    type: Literal[FinancialRatioType.SECURED] = FinancialRatioType.SECURED
    ratio: float = Field(..., description="The ratio multiplier")


class TotalNetRatioValue(BaseModel):
    """Total Net Leverage Ratio"""
    type: Literal[FinancialRatioType.TOTAL_NET] = FinancialRatioType.TOTAL_NET
    ratio: float = Field(..., description="The ratio multiplier")


class FixedChargeRatioValue(BaseModel):
    """Fixed Charge Coverage Ratio"""
    type: Literal[FinancialRatioType.FIXED_CHARGE] = FinancialRatioType.FIXED_CHARGE
    ratio: float = Field(..., description="The ratio multiplier")


class InterestCoverageRatioValue(BaseModel):
    """Interest Coverage Ratio"""
    type: Literal[FinancialRatioType.INTEREST_COVERAGE] = FinancialRatioType.INTEREST_COVERAGE
    ratio: float = Field(..., description="The ratio multiplier")


class NoCovenantValue(BaseModel):
    """N/A, no financial covenant for the instrument"""
    type: Literal[FinancialRatioType.NO_COVENANT] = FinancialRatioType.NO_COVENANT


class RatioNotStatedValue(BaseModel):
    """Not stated in Term Sheet"""
    type: Literal[FinancialRatioType.NOT_STATED] = FinancialRatioType.NOT_STATED


# Composite member 4: Percentage with Conditions
class PercentageConditionType(str, Enum):
    """Type discriminator for percentage with conditions composite"""
    WITH_LEVERAGE_TEST = "with_leverage_test"
    NO_LEVERAGE_TEST = "no_leverage_test"
    BASKET_NO_COMPONENT = "basket_no_component"
    NO_BASKET = "no_basket"
    NOT_STATED = "not_stated"


class LeverageTestModel(BaseModel):
    """Details for leverage test"""
    multiplier: float = Field(..., description="The multiplier value")
    metric: str = Field(..., description="The metric to which the multiplier applies")


class PercentageWithLeverageTestValue(BaseModel):
    """Percentage with leverage test"""
    type: Literal[PercentageConditionType.WITH_LEVERAGE_TEST] = PercentageConditionType.WITH_LEVERAGE_TEST
    percentage: float = Field(..., description="The percentage value")
    test: LeverageTestModel = Field(..., description="The leverage test details")


class PercentageNoLeverageTestValue(BaseModel):
    """Percentage with no leverage test"""
    type: Literal[PercentageConditionType.NO_LEVERAGE_TEST] = PercentageConditionType.NO_LEVERAGE_TEST
    percentage: float = Field(..., description="The percentage value")


class BasketNoComponentValue(BaseModel):
    """N/A, basket present but component not present"""
    type: Literal[PercentageConditionType.BASKET_NO_COMPONENT] = PercentageConditionType.BASKET_NO_COMPONENT


class NoBasketValue(BaseModel):
    """N/A, basket not present"""
    type: Literal[PercentageConditionType.NO_BASKET] = PercentageConditionType.NO_BASKET


class PercentageConditionNotStatedValue(BaseModel):
    """Not stated in Term Sheet"""
    type: Literal[PercentageConditionType.NOT_STATED] = PercentageConditionType.NOT_STATED


class FinancialDataModel(BaseModel):
    """
    Pydantic model for API request/response schemas
    """
    id: Optional[int] = None
    boolean_value: Optional[bool] = Field(None, description="A boolean Yes or No value")
    term_sheet_status: Optional[TermSheetStatus] = Field(None, description="Term sheet status option")
    numeric_value: Optional[float] = Field(None, description="A numeric value")
    date_value: Optional[date] = Field(None, description="A date value")
    
    # Original composite value
    composite_value: Optional[Union[NumberValue, GreaterOfValue, NoMinimumValue, NoPikValue]] = Field(
        None, 
        description="A composite value that can be one of several types"
    )
    
    # New composite members
    percentage_multiple: Optional[Union[PercentageMultipleValue, NoCashRequirementValue, PercentageNotStatedValue]] = Field(
        None,
        description="Percentage multiple composite value"
    )
    
    names_list: Optional[Union[NamesListValue, NamesListNAValue]] = Field(
        None,
        description="Names list composite value"
    )
    
    financial_ratio: Optional[Union[
        FirstLienRatioValue,
        SeniorSecuredRatioValue,
        SecuredRatioValue,
        TotalNetRatioValue,
        FixedChargeRatioValue,
        InterestCoverageRatioValue,
        NoCovenantValue,
        RatioNotStatedValue
    ]] = Field(
        None,
        description="Financial ratio composite value"
    )
    
    percentage_condition: Optional[Union[
        PercentageWithLeverageTestValue,
        PercentageNoLeverageTestValue,
        BasketNoComponentValue,
        NoBasketValue,
        PercentageConditionNotStatedValue
    ]] = Field(
        None,
        description="Percentage with conditions composite value"
    )
    
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
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
        }
