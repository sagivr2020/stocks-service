import asyncio
from typing import Dict, Any

from .polygon_service import PolygonService
from .marketwatch_scraper import MarketWatchScraper

class StockService:    
    def __init__(self, polygon_api_key: str):
        self.polygon_service = PolygonService(polygon_api_key)
        self.marketwatch_scraper = MarketWatchScraper()
        self._stock_amounts: Dict[str, int] = {}
    
    async def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        symbol = symbol.upper()
        
        try:
            polygon_task = self.polygon_service.get_daily_open_close(symbol)
            performance_task = self.marketwatch_scraper.get_stock_performance(symbol)
            
            polygon_data, performance_data = await asyncio.gather(
                polygon_task, performance_task, return_exceptions=True
            )

            if isinstance(polygon_data, Exception):
                raise ValueError(f"Failed to fetch stock data from Polygon.io: {polygon_data}")
            
            if isinstance(performance_data, Exception):
                performance_data = {
                    "5 Day": "N/A",
                    "1 Month": "N/A",
                    "3 Month": "N/A", 
                    "YTD": "N/A",
                    "1 Year": "N/A",
                    "note": "Performance data unavailable"
                }
            
            stock_data = {
                "afterHours": polygon_data["afterHours"],
                "close": polygon_data["close"],
                "from": polygon_data["from"],
                "high": polygon_data["high"],
                "low": polygon_data["low"],
                "open": polygon_data["open"],
                "preMarket": polygon_data["preMarket"],
                "status": polygon_data["status"],
                "symbol": polygon_data["symbol"],
                "volume": int(polygon_data["volume"]),
                "performance": performance_data,
                "amount": self._stock_amounts.get(symbol, 0)
            }
            
            return stock_data
            
        except Exception as e:
            raise
    
    async def update_stock_amount(self, symbol: str, amount: int) -> str:
        symbol = symbol.upper()

        current_amount = self._stock_amounts.get(symbol, 0)
        self._stock_amounts[symbol] = current_amount + amount
        
        message = f"{amount} units of stock {symbol} were added to your stock record"
        
        return message
    
    def get_stock_amount(self, symbol: str) -> int:
        return self._stock_amounts.get(symbol.upper(), 0)
