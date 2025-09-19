
import pytest
from unittest.mock import AsyncMock, patch

from src.services.stock_service import StockService


class TestStockService:
    
    @pytest.fixture
    def stock_service(self):
        return StockService("test_api_key")
    
    @pytest.fixture
    def mock_polygon_data(self):
        return {
            "status": "OK",
            "from": "2024-01-09",
            "symbol": "AAPL",
            "open": 130.465,
            "high": 133.41,
            "low": 129.89,
            "close": 130.15,
            "volume": 70790813,
            "afterHours": 129.85,
            "preMarket": 129.6
        }
    
    @pytest.fixture
    def mock_performance_data(self):
        return {
            "5 Day": "1.23%",
            "1 Month": "5.67%",
            "3 Month": "12.34%",
            "YTD": "23.45%",
            "1 Year": "34.56%"
        }
    
    @pytest.mark.asyncio
    async def test_get_stock_data_success(self, stock_service, mock_polygon_data, mock_performance_data):
        with patch.object(stock_service.polygon_service, 'get_daily_open_close', new_callable=AsyncMock) as mock_polygon:
            with patch.object(stock_service.marketwatch_scraper, 'get_stock_performance', new_callable=AsyncMock) as mock_marketwatch:
                mock_polygon.return_value = mock_polygon_data
                mock_marketwatch.return_value = mock_performance_data
                
                result = await stock_service.get_stock_data("AAPL")
                
                assert result["symbol"] == "AAPL"
                assert result["close"] == 130.15
                assert result["volume"] == 70790813
                assert result["performance"] == mock_performance_data
                assert result["amount"] == 0
                
                mock_polygon.assert_called_once_with("AAPL")
                mock_marketwatch.assert_called_once_with("AAPL")
    
    @pytest.mark.asyncio
    async def test_get_stock_data_polygon_failure(self, stock_service, mock_performance_data):
        with patch.object(stock_service.polygon_service, 'get_daily_open_close', new_callable=AsyncMock) as mock_polygon:
            with patch.object(stock_service.marketwatch_scraper, 'get_stock_performance', new_callable=AsyncMock) as mock_marketwatch:
                mock_polygon.side_effect = ValueError("API error")
                mock_marketwatch.return_value = mock_performance_data
                
                with pytest.raises(ValueError, match="Failed to fetch stock data from Polygon.io"):
                    await stock_service.get_stock_data("AAPL")
    
    @pytest.mark.asyncio
    async def test_get_stock_data_marketwatch_failure(self, stock_service, mock_polygon_data):
        with patch.object(stock_service.polygon_service, 'get_daily_open_close', new_callable=AsyncMock) as mock_polygon:
            with patch.object(stock_service.marketwatch_scraper, 'get_stock_performance', new_callable=AsyncMock) as mock_marketwatch:
                mock_polygon.return_value = mock_polygon_data
                mock_marketwatch.side_effect = ValueError("Scraping error")
                
                result = await stock_service.get_stock_data("AAPL")
                
                assert result["symbol"] == "AAPL"
                assert result["close"] == 130.15
                assert result["performance"]["5 Day"] == "N/A"
                assert "note" in result["performance"]
    
    @pytest.mark.asyncio
    async def test_get_stock_data_with_existing_amount(self, stock_service, mock_polygon_data, mock_performance_data):
        stock_service._stock_amounts["AAPL"] = 10
        
        with patch.object(stock_service.polygon_service, 'get_daily_open_close', new_callable=AsyncMock) as mock_polygon:
            with patch.object(stock_service.marketwatch_scraper, 'get_stock_performance', new_callable=AsyncMock) as mock_marketwatch:
                mock_polygon.return_value = mock_polygon_data
                mock_marketwatch.return_value = mock_performance_data
                
                result = await stock_service.get_stock_data("AAPL")
                
                assert result["amount"] == 10
