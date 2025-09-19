# Stocks REST API

A FastAPI-based REST API that retrieves stock data from Polygon.io and scrapes performance data from MarketWatch.

## Features

- **GET /stock/{stock_symbol}**: Retrieve comprehensive stock data
- **POST /stock/{stock_symbol}**: Update stock purchase amount
- Docker containerization
- Full test coverage

## Architecture

```
src/
├── api/
│   ├── routes.py          # FastAPI route definitions
│   └── __init__.py
├── models/
│   ├── stock.py           # Pydantic models
│   └── __init__.py
├── services/
│   ├── polygon_service.py     # Polygon.io API client
│   ├── marketwatch_scraper.py # MarketWatch web scraper
│   ├── stock_service.py       # Main orchestration service
│   └── __init__.py
├── main.py                # FastAPI application
└── __init__.py

tests/
├── test_models.py
├── test_polygon_service.py
├── test_marketwatch_scraper.py
├── test_stock_service.py
└── test_api_routes.py
```

## Stock Model

Each stock contains the following attributes:

- `afterHours`: float - After hours trading price (Polygon.io)
- `close`: float - Closing price (Polygon.io)
- `from`: str - Date in YYYY-MM-DD format (Polygon.io)
- `high`: float - Highest price of the day (Polygon.io)
- `low`: float - Lowest price of the day (Polygon.io)
- `open`: float - Opening price (Polygon.io)
- `preMarket`: float - Pre-market trading price (Polygon.io)
- `status`: str - Status of the stock data (Polygon.io)
- `symbol`: str - Stock symbol (Polygon.io)
- `volume`: int - Trading volume (Polygon.io)
- `performance`: dict - Performance data (MarketWatch)
- `amount`: int - User's stock amount (default: 0)

## API Endpoints

### GET /stock/{stock_symbol}

Retrieves complete stock data for the given symbol.

**Example Request:**
```bash
curl http://localhost:8000/stock/AAPL
```

**Note:** The API uses January 9, 2024 as the default date for fetching stock data from Polygon.io.

**Example Response:**
```json
{
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
```

### POST /stock/{stock_symbol}

Updates the stock amount for the given symbol.

**Example Request:**
```bash
curl -X POST http://localhost:8000/stock/AAPL \
  -H "Content-Type: application/json" \
  -d '{"amount": 5}'
```

**Example Response:**
```json
{
  "message": "5 units of stock AAPL were added to your stock record"
}
```

## Installation & Usage

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Run tests:**
```bash
pytest
```

### Docker

1. **Build the image:**
```bash
docker build -t stocks-api .
```

2. **Run the container:**
```bash
docker run -p 8000:8000 stocks-api
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive API docs:** http://localhost:8000/docs


## Concurrency

The application uses async/await for concurrent operations:
- Polygon.io API calls and MarketWatch scraping run in parallel
- Non-blocking I/O operations

## Testing

Comprehensive test suite covering:
- Service layer logic
- API endpoint behavior

Run tests with:
```bash
pytest -v
```
