from typing import Dict, Any

import httpx
from bs4 import BeautifulSoup
import requests

class MarketWatchScraper:    
    def __init__(self):
        self.base_url = "https://www.marketwatch.com"
        
    async def get_stock_performance(self, symbol: str) -> Dict[str, Any]:
        url = f"{self.base_url}/investing/stock/{symbol.lower()}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
            try:
                response = await client.get(url, headers=headers)

                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                performance_data = {}
                
                performance_data = self._extract_performance_table(soup)
                
                if not performance_data:
                    performance_data = self._get_fallback_performance_data()
                
                return performance_data
                
            except Exception as e:
                return self._get_fallback_performance_data()
    
    def _extract_performance_table(self, soup: BeautifulSoup) -> Dict[str, Any]:
        performance_data = {}        
        performance_sections = soup.find_all(string=lambda text: text and 
                                           any(keyword in text.upper() for keyword in 
                                               ["Performance", "KEY DATA"]))
        
        for section in performance_sections:
            parent = section.parent
            if parent:
                table = parent.find_next("table") or parent.find_parent("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        cells = row.find_all(["td", "th"])
                        if len(cells) >= 2:
                            key = cells[0].get_text(strip=True)
                            value = cells[1].get_text(strip=True)
                            if key and value and any(period in key for period in 
                                                   ["Day", "Week", "Month", "Year", "YTD"]):
                                performance_data[key] = value
        
        return performance_data
    
    def _get_fallback_performance_data(self) -> Dict[str, Any]:
        return {
            "5 Day": "N/A",
            "1 Month": "N/A", 
            "3 Month": "N/A",
            "YTD": "N/A",
            "1 Year": "N/A",
            "note": "Performance data unavailable - scraping failed"
        }
