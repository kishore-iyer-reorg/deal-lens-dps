from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum
import json
from typing import Optional, Dict, Any, List, Union
from datetime import date


class TermSheetStatus(str, Enum):
    YES = "Yes"
    PARTIAL = "Partial"
    NO = "No"
    NA = "N/A"
    NOT_STATED = "Not stated in Term Sheet"


class CompositeValueType(str, Enum):
    NUMBER = "number"
    GREATER_OF = "greater_of"
    NO_MINIMUM = "no_minimum"
    NO_PIK = "no_pik"


class PercentageMultipleType(str, Enum):
    PERCENTAGE = "percentage"
    NO_CASH_REQUIREMENT = "no_cash_requirement"
    NOT_STATED = "not_stated"


class NamesListType(str, Enum):
    NAMES_LIST = "names_list"
    NA = "na"


class FinancialRatioType(str, Enum):
    FIRST_LIEN = "first_lien"
    SENIOR_SECURED = "senior_secured"
    SECURED = "secured"
    TOTAL_NET = "total_net"
    FIXED_CHARGE = "fixed_charge"
    INTEREST_COVERAGE = "interest_coverage"
    NO_COVENANT = "no_covenant"
    NOT_STATED = "not_stated"


class PercentageConditionType(str, Enum):
    WITH_LEVERAGE_TEST = "with_leverage_test"
    NO_LEVERAGE_TEST = "no_leverage_test"
    BASKET_NO_COMPONENT = "basket_no_component"
    NO_BASKET = "no_basket"
    NOT_STATED = "not_stated"


class FinancialData(models.Model):
    """
    Tortoise ORM model for financial data storage
    """
    id = fields.IntField(pk=True)
    boolean_value = fields.BooleanField(null=True)
    term_sheet_status = fields.CharEnumField(
        TermSheetStatus, null=True, max_length=30
    )
    numeric_value = fields.FloatField(null=True)
    date_value = fields.DateField(null=True)
    
    # Store composite values as JSON fields
    # Original composite value
    composite_value_type = fields.CharEnumField(
        CompositeValueType, null=True, max_length=20
    )
    composite_value_data = fields.JSONField(null=True)
    
    # Percentage multiple composite
    percentage_multiple_type = fields.CharEnumField(
        PercentageMultipleType, null=True, max_length=30
    )
    percentage_multiple_data = fields.JSONField(null=True)
    
    # Names list composite
    names_list_type = fields.CharEnumField(
        NamesListType, null=True, max_length=15
    )
    names_list_data = fields.JSONField(null=True)
    
    # Financial ratio composite
    financial_ratio_type = fields.CharEnumField(
        FinancialRatioType, null=True, max_length=30
    )
    financial_ratio_data = fields.JSONField(null=True)
    
    # Percentage with conditions composite
    percentage_condition_type = fields.CharEnumField(
        PercentageConditionType, null=True, max_length=30
    )
    percentage_condition_data = fields.JSONField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "financial_data"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary format with composite values structured properly"""
        result = {
            "id": self.id,
            "boolean_value": self.boolean_value,
            "term_sheet_status": self.term_sheet_status.value if self.term_sheet_status else None,
            "numeric_value": self.numeric_value,
            "date_value": str(self.date_value) if self.date_value else None,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        
        # Handle composite value
        if self.composite_value_type:
            composite_value = {"type": self.composite_value_type.value}
            if self.composite_value_type == CompositeValueType.NUMBER:
                composite_value["value"] = self.composite_value_data.get("value")
            elif self.composite_value_type == CompositeValueType.GREATER_OF:
                composite_value["details"] = self.composite_value_data.get("details")
            result["composite_value"] = composite_value
        
        # Handle percentage multiple composite
        if self.percentage_multiple_type:
            percentage_multiple = {"type": self.percentage_multiple_type.value}
            if self.percentage_multiple_type == PercentageMultipleType.PERCENTAGE:
                percentage_multiple["value"] = self.percentage_multiple_data.get("value")
            result["percentage_multiple"] = percentage_multiple
        
        # Handle names list composite
        if self.names_list_type:
            names_list = {"type": self.names_list_type.value}
            if self.names_list_type == NamesListType.NAMES_LIST:
                names_list["names"] = self.names_list_data.get("names")
            result["names_list"] = names_list
        
        # Handle financial ratio composite
        if self.financial_ratio_type:
            financial_ratio = {"type": self.financial_ratio_type.value}
            if self.financial_ratio_type not in [FinancialRatioType.NO_COVENANT, FinancialRatioType.NOT_STATED]:
                financial_ratio["ratio"] = self.financial_ratio_data.get("ratio")
            result["financial_ratio"] = financial_ratio
        
        # Handle percentage condition composite
        if self.percentage_condition_type:
            percentage_condition = {"type": self.percentage_condition_type.value}
            if self.percentage_condition_type == PercentageConditionType.WITH_LEVERAGE_TEST:
                percentage_condition["percentage"] = self.percentage_condition_data.get("percentage")
                percentage_condition["test"] = self.percentage_condition_data.get("test")
            elif self.percentage_condition_type == PercentageConditionType.NO_LEVERAGE_TEST:
                percentage_condition["percentage"] = self.percentage_condition_data.get("percentage")
            result["percentage_condition"] = percentage_condition
        
        return result
