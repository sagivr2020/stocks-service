import pytest
from pydantic import ValidationError

from src.models.stock import Stock, StockUpdateRequest, StockUpdateResponse


class TestStock:    
    def test_stock_model_valid_data(self):
        stock_data = {
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
                "YTD": "23.45%"
            },
            "amount": 5
        }
        
        stock = Stock(**stock_data)
        
        assert stock.afterHours == 129.85
        assert stock.close == 130.15
        assert stock.from_ == "2024-01-09"
        assert stock.high == 133.41
        assert stock.low == 129.89
        assert stock.open == 130.465
        assert stock.preMarket == 129.6
        assert stock.status == "OK"
        assert stock.symbol == "AAPL"
        assert stock.volume == 70790813
        assert stock.performance == {"5 Day": "1.23%", "1 Month": "5.67%", "YTD": "23.45%"}
        assert stock.amount == 5
    
    def test_stock_model_default_amount(self):
        stock_data = {
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
            "performance": {}
        }
        
        stock = Stock(**stock_data)
        assert stock.amount == 0  # Default value
    
    def test_stock_model_missing_required_field(self):
        stock_data = {
            "afterHours": 129.85,
            "close": 130.15,
            # Missing "from" field
            "high": 133.41,
            "low": 129.89,
            "open": 130.465,
            "preMarket": 129.6,
            "status": "OK",
            "symbol": "AAPL",
            "volume": 70790813,
            "performance": {}
        }
        
        with pytest.raises(ValidationError):
            Stock(**stock_data)

