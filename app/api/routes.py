from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional, Dict, Any

from app.models.financial_data import FinancialData
from app.models.pydantic_models import (
    FinancialDataModel,
    CompositeValueType,
    PercentageMultipleType,
    NamesListType,
    FinancialRatioType,
    PercentageConditionType
)

router = APIRouter()


@router.post("/financial_data/", response_model=FinancialDataModel, status_code=status.HTTP_201_CREATED)
async def create_financial_data(data: FinancialDataModel):
    """
    Create a new financial data record.
    """
    # Create a new record in the database
    financial_data = await FinancialData.create(
        boolean_value=data.boolean_value,
        term_sheet_status=data.term_sheet_status.value if data.term_sheet_status else None,
        numeric_value=data.numeric_value,
        date_value=data.date_value,
    )
    
    # Process composite value field
    if data.composite_value:
        financial_data.composite_value_type = data.composite_value.type
        
        if data.composite_value.type == CompositeValueType.NUMBER:
            financial_data.composite_value_data = {"value": data.composite_value.value}
        elif data.composite_value.type == CompositeValueType.GREATER_OF:
            financial_data.composite_value_data = {"details": data.composite_value.details.dict()}
        else:
            financial_data.composite_value_data = {}
    
    # Process percentage multiple field
    if data.percentage_multiple:
        financial_data.percentage_multiple_type = data.percentage_multiple.type
        
        if data.percentage_multiple.type == PercentageMultipleType.PERCENTAGE:
            financial_data.percentage_multiple_data = {"value": data.percentage_multiple.value}
        else:
            financial_data.percentage_multiple_data = {}
    
    # Process names list field
    if data.names_list:
        financial_data.names_list_type = data.names_list.type
        
        if data.names_list.type == NamesListType.NAMES_LIST:
            financial_data.names_list_data = {"names": data.names_list.names}
        else:
            financial_data.names_list_data = {}
    
    # Process financial ratio field
    if data.financial_ratio:
        financial_data.financial_ratio_type = data.financial_ratio.type
        
        if data.financial_ratio.type not in [FinancialRatioType.NO_COVENANT, FinancialRatioType.NOT_STATED]:
            financial_data.financial_ratio_data = {"ratio": data.financial_ratio.ratio}
        else:
            financial_data.financial_ratio_data = {}
    
    # Process percentage condition field
    if data.percentage_condition:
        financial_data.percentage_condition_type = data.percentage_condition.type
        
        if data.percentage_condition.type == PercentageConditionType.WITH_LEVERAGE_TEST:
            financial_data.percentage_condition_data = {
                "percentage": data.percentage_condition.percentage,
                "test": data.percentage_condition.test.dict()
            }
        elif data.percentage_condition.type == PercentageConditionType.NO_LEVERAGE_TEST:
            financial_data.percentage_condition_data = {
                "percentage": data.percentage_condition.percentage
            }
        else:
            financial_data.percentage_condition_data = {}
    
    # Save the updated record
    await financial_data.save()
    
    # Convert to dictionary with properly formatted composite values
    return FinancialDataModel.parse_obj(financial_data.to_dict())


@router.get("/financial_data/", response_model=List[FinancialDataModel])
async def get_all_financial_data(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get all financial data records with pagination.
    """
    records = await FinancialData.all().offset(offset).limit(limit)
    return [FinancialDataModel.parse_obj(record.to_dict()) for record in records]


@router.get("/financial_data/{record_id}", response_model=FinancialDataModel)
async def get_financial_data(record_id: int):
    """
    Get a specific financial data record by ID.
    """
    record = await FinancialData.get_or_none(id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Financial data record with ID {record_id} not found")
    
    return FinancialDataModel.parse_obj(record.to_dict())


@router.put("/financial_data/{record_id}", response_model=FinancialDataModel)
async def update_financial_data(record_id: int, data: FinancialDataModel):
    """
    Update a specific financial data record.
    """
    record = await FinancialData.get_or_none(id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Financial data record with ID {record_id} not found")
    
    # Update basic fields
    record.boolean_value = data.boolean_value
    record.term_sheet_status = data.term_sheet_status.value if data.term_sheet_status else None
    record.numeric_value = data.numeric_value
    record.date_value = data.date_value
    
    # Process composite value field
    if data.composite_value:
        record.composite_value_type = data.composite_value.type
        
        if data.composite_value.type == CompositeValueType.NUMBER:
            record.composite_value_data = {"value": data.composite_value.value}
        elif data.composite_value.type == CompositeValueType.GREATER_OF:
            record.composite_value_data = {"details": data.composite_value.details.dict()}
        else:
            record.composite_value_data = {}
    else:
        record.composite_value_type = None
        record.composite_value_data = None
    
    # Process percentage multiple field
    if data.percentage_multiple:
        record.percentage_multiple_type = data.percentage_multiple.type
        
        if data.percentage_multiple.type == PercentageMultipleType.PERCENTAGE:
            record.percentage_multiple_data = {"value": data.percentage_multiple.value}
        else:
            record.percentage_multiple_data = {}
    else:
        record.percentage_multiple_type = None
        record.percentage_multiple_data = None
    
    # Process names list field
    if data.names_list:
        record.names_list_type = data.names_list.type
        
        if data.names_list.type == NamesListType.NAMES_LIST:
            record.names_list_data = {"names": data.names_list.names}
        else:
            record.names_list_data = {}
    else:
        record.names_list_type = None
        record.names_list_data = None
    
    # Process financial ratio field
    if data.financial_ratio:
        record.financial_ratio_type = data.financial_ratio.type
        
        if data.financial_ratio.type not in [FinancialRatioType.NO_COVENANT, FinancialRatioType.NOT_STATED]:
            record.financial_ratio_data = {"ratio": data.financial_ratio.ratio}
        else:
            record.financial_ratio_data = {}
    else:
        record.financial_ratio_type = None
        record.financial_ratio_data = None
    
    # Process percentage condition field
    if data.percentage_condition:
        record.percentage_condition_type = data.percentage_condition.type
        
        if data.percentage_condition.type == PercentageConditionType.WITH_LEVERAGE_TEST:
            record.percentage_condition_data = {
                "percentage": data.percentage_condition.percentage,
                "test": data.percentage_condition.test.dict()
            }
        elif data.percentage_condition.type == PercentageConditionType.NO_LEVERAGE_TEST:
            record.percentage_condition_data = {
                "percentage": data.percentage_condition.percentage
            }
        else:
            record.percentage_condition_data = {}
    else:
        record.percentage_condition_type = None
        record.percentage_condition_data = None
    
    # Save the updated record
    await record.save()
    
    # Return the updated record
    return FinancialDataModel.parse_obj(record.to_dict())


@router.delete("/financial_data/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_financial_data(record_id: int):
    """
    Delete a specific financial data record.
    """
    record = await FinancialData.get_or_none(id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Financial data record with ID {record_id} not found")
    
    await record.delete()
    return
