from typing import Dict, Any

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..models import Stock, StockUpdateRequest, StockUpdateResponse
from ..services.stock_service import StockService

POLYGON_API_KEY = "bs1n5Vdqoi_NOvmCZ_85rrcvtFnYN3vm"
stock_service = StockService(POLYGON_API_KEY)

router = APIRouter(prefix="/stock", tags=["stocks"])

@router.get("/{stock_symbol}", response_model=Stock)
async def get_stock(stock_symbol: str) -> Dict[str, Any]:
    try:        
        stock_data = await stock_service.get_stock_data(stock_symbol)        
        return stock_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while fetching stock data"
        )


@router.post("/{stock_symbol}", status_code=status.HTTP_201_CREATED)
async def update_stock(stock_symbol: str, request: StockUpdateRequest) -> JSONResponse:
    try:
        message = await stock_service.update_stock_amount(stock_symbol, request.amount)
        response_data = StockUpdateResponse(message=message)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response_data.model_dump()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating stock amount"
        )
