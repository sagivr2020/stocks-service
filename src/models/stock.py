from typing import Dict, Any
from pydantic import BaseModel, Field


class Stock(BaseModel):    
    afterHours: float = Field(description="After hours trading price")
    close: float = Field(description="Closing price")
    from_: str = Field(alias="from", description="Date in YYYY-MM-DD format")
    high: float = Field(description="Highest price of the day")
    low: float = Field(description="Lowest price of the day")
    open: float = Field(description="Opening price")
    preMarket: float = Field(description="Pre-market trading price")
    status: str = Field(description="Status of the stock data")
    symbol: str = Field(description="Stock symbol")
    volume: int = Field(description="Trading volume")
    performance: Dict[str, Any] = Field(description="Performance data from MarketWatch")
    amount: int = Field(default=0, description="Amount of stocks purchased")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "afterHours": 129.85,
                "close": 130.15,
                "from": "2024-01-09",
                "high": 133.41,
                "low": 129.89,
                "open": 130.465,
                "preMarket": 129.6,
                "status": "OK",
                "symbol": "AAPL",
                "volume": 70790813,
                "performance": {
                    "5 Day": "1.23%",
                    "1 Month": "5.67%",
                    "3 Month": "12.34%",
                    "YTD": "23.45%",
                    "1 Year": "34.56%"
                },
                "amount": 0
            }
        }
    }


class StockUpdateRequest(BaseModel):    
    amount: int = Field(description="Amount of stocks to add", ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": 5
            }
        }
    }


class StockUpdateResponse(BaseModel):    
    message: str = Field(description="Success message")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "5 units of stock AAPL were added to your stock record"
            }
        }
    }
