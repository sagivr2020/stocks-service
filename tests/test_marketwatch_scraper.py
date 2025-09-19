import pytest
from unittest.mock import AsyncMock, patch
import httpx

from src.services.marketwatch_scraper import MarketWatchScraper


class TestMarketWatchScraper:    
    @pytest.fixture
    def scraper(self):
        return MarketWatchScraper()
    
    @pytest.fixture
    def mock_html_with_performance(self):
        return """
        <html>
            <body>
                <div>
                    <h3>Performance</h3>
                    <table>
                        <tr><td>5 Day</td><td>1.23%</td></tr>
                        <tr><td>1 Month</td><td>5.67%</td></tr>
                        <tr><td>3 Month</td><td>12.34%</td></tr>
                        <tr><td>YTD</td><td>23.45%</td></tr>
                        <tr><td>1 Year</td><td>34.56%</td></tr>
                    </table>
                </div>
            </body>
        </html>
        """
    
    @pytest.fixture
    def mock_html_without_performance(self):
        return """
        <html>
            <body>
                <div>
                    <h1>Stock Page</h1>
                    <p>Some other content</p>
                </div>
            </body>
        </html>
        """
    
    @pytest.mark.asyncio
    async def test_get_stock_performance_success(self, scraper, mock_html_with_performance):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.raise_for_status.return_value = None
            mock_response.content = mock_html_with_performance.encode()
            mock_get.return_value = mock_response
            
            result = await scraper.get_stock_performance("AAPL")
            
            assert "5 Day" in result
            assert "1 Month" in result
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_stock_performance_no_data_found(self, scraper, mock_html_without_performance):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.raise_for_status.return_value = None
            mock_response.content = mock_html_without_performance.encode()
            mock_get.return_value = mock_response
            
            result = await scraper.get_stock_performance("AAPL")
            
            assert "5 Day" in result
            assert "1 Month" in result
            assert result["5 Day"] == "N/A"
            assert result["note"] == "Performance data unavailable - scraping failed"
    
    @pytest.mark.asyncio
    async def test_get_stock_performance_request_error(self, scraper):
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.RequestError("Connection failed")
            
            result = await scraper.get_stock_performance("AAPL")
            
            assert "5 Day" in result
            assert result["5 Day"] == "N/A"
    
    def test_get_fallback_performance_data(self, scraper):
        fallback_data = scraper._get_fallback_performance_data()
        
        expected_keys = ["5 Day", "1 Month", "3 Month", "YTD", "1 Year", "note"]
        for key in expected_keys:
            assert key in fallback_data
        
        assert fallback_data["note"] == "Performance data unavailable - scraping failed"

