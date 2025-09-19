from datetime import datetime
from typing import Dict, Any, Optional

import httpx


class PolygonService:    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        
    async def get_daily_open_close(self, symbol: str, date: Optional[str] = None) -> Dict[str, Any]:
        if date is None:
            date = "2024-01-09"  # Default to January 9, 2024
            
        url = f"{self.base_url}/v1/open-close/{symbol.upper()}/{date}"
        params = {"apiKey": self.api_key}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                required_fields = [
                    "status", "from", "symbol", "open", "high", "low", 
                    "close", "volume", "afterHours", "preMarket"
                ]
                
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Missing required field '{field}' in API response")
                return data
                
            except Exception as e:
                raise ValueError(f"Unexpected error: {e}")
