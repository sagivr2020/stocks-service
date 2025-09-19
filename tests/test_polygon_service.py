import pytest
from unittest.mock import patch, MagicMock
import httpx

from src.services.polygon_service import PolygonService


class TestPolygonService:
    
    @pytest.fixture
    def polygon_service(self):
        return PolygonService("test_api_key")
    
    @pytest.fixture
    def mock_polygon_response(self):
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
    
    @pytest.mark.asyncio
    async def test_get_daily_open_close_success(self, polygon_service, mock_polygon_response):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value=mock_polygon_response)
            mock_get.return_value = mock_response
            
            result = await polygon_service.get_daily_open_close("AAPL", "2024-01-09")
            
            assert result == mock_polygon_response
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_daily_open_close_with_default_date(self, polygon_service, mock_polygon_response):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value=mock_polygon_response)
            mock_get.return_value = mock_response
            
            result = await polygon_service.get_daily_open_close("AAPL")
            
            assert result == mock_polygon_response
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_daily_open_close_missing_field(self, polygon_service):
        incomplete_response = {
            "status": "OK",
            "from": "2024-01-09",
            "symbol": "AAPL",
        }
        
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value=incomplete_response)
            mock_get.return_value = mock_response
            
            with pytest.raises(ValueError, match="Missing required field"):
                await polygon_service.get_daily_open_close("AAPL")

