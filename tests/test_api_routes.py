import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from src.main import app


class TestStockRoutes:    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def mock_stock_data(self):
        return {
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
            "amount": 0
        }
    
    def test_get_stock_success(self, client, mock_stock_data):
        with patch("src.api.routes.stock_service.get_stock_data", new_callable=AsyncMock) as mock_get_stock:
            mock_get_stock.return_value = mock_stock_data
            
            response = client.get("/stock/AAPL")
            
            assert response.status_code == 200
            data = response.json()
            assert data["symbol"] == "AAPL"
            assert data["close"] == 130.15
            assert data["performance"]["5 Day"] == "1.23%"
            mock_get_stock.assert_called_once_with("AAPL")
    
    def test_get_stock_not_found(self, client):
        with patch("src.api.routes.stock_service.get_stock_data", new_callable=AsyncMock) as mock_get_stock:
            mock_get_stock.side_effect = ValueError("Stock symbol 'INVALID' not found")
            
            response = client.get("/stock/INVALID")
            
            assert response.status_code == 404
            data = response.json()
            assert "Stock symbol 'INVALID' not found" in data["detail"]
    
    def test_get_stock_server_error(self, client):
        with patch("src.api.routes.stock_service.get_stock_data", new_callable=AsyncMock) as mock_get_stock:
            mock_get_stock.side_effect = Exception("Unexpected error")
            
            response = client.get("/stock/AAPL")
            
            assert response.status_code == 500
            data = response.json()
            assert "Internal server error" in data["detail"]
    
    def test_post_stock_success(self, client):
        with patch("src.api.routes.stock_service.update_stock_amount", new_callable=AsyncMock) as mock_update:
            mock_update.return_value = "5 units of stock AAPL were added to your stock record"
            
            response = client.post("/stock/AAPL", json={"amount": 5})
            
            assert response.status_code == 201
            data = response.json()
            assert data["message"] == "5 units of stock AAPL were added to your stock record"
            mock_update.assert_called_once_with("AAPL", 5)

    def test_post_stock_server_error(self, client):
        with patch("src.api.routes.stock_service.update_stock_amount", new_callable=AsyncMock) as mock_update:
            mock_update.side_effect = Exception("Unexpected error")
            
            response = client.post("/stock/AAPL", json={"amount": 5})
            
            assert response.status_code == 500
            data = response.json()
            assert "Internal server error" in data["detail"]
