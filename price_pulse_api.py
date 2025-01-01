# price_pulse_api.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict
from enum import Enum
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PricePulseAPI")

app = FastAPI(
    title="PricePulse API",
    description="Maximize profits with real-time pricing intelligence.",
    version="1.0.0"
)

# Enums for seasonality
class Seasonality(str, Enum):
    spring = "spring"
    summer = "summer"
    autumn = "autumn"
    winter = "winter"

# Models
class DemandIndicators(BaseModel):
    search_trends: int = Field(..., ge=0, le=100, description="Search trends index (0-100)")
    seasonality: Seasonality

class ProductData(BaseModel):
    product_id: str = Field(..., description="Unique identifier for the product")
    current_price: float = Field(..., gt=0, description="Current price of the product")
    inventory_level: int = Field(..., ge=0, description="Current inventory level")
    competitor_prices: List[float] = Field(..., min_items=1, description="List of competitor prices")
    demand_indicators: DemandIndicators

class SinglePriceRecommendation(BaseModel):
    product_id: str
    recommended_price: float
    expected_sales_volume: int
    profit_margin: float

class OptimizePriceResponse(BaseModel):
    product_id: str
    recommended_price: float
    expected_sales_volume: int
    profit_margin: float

class BulkOptimizeRequest(BaseModel):
    products: List[ProductData]

class BulkOptimizeResponse(BaseModel):
    recommendations: List[OptimizePriceResponse]

# Utility Functions
def calculate_recommended_price(product: ProductData) -> OptimizePriceResponse:
    try:
        # Simple algorithm for demonstration purposes
        average_competitor_price = sum(product.competitor_prices) / len(product.competitor_prices)
        price_adjustment = (average_competitor_price - product.current_price) * 0.5

        # Demand factor based on search trends and seasonality
        seasonality_factor = {
            "spring": 1.0,
            "summer": 1.1,
            "autumn": 0.9,
            "winter": 1.05
        }[product.demand_indicators.seasonality]

        demand_factor = (product.demand_indicators.search_trends / 100) * seasonality_factor

        recommended_price = product.current_price + price_adjustment * demand_factor
        recommended_price = round(recommended_price, 2)

        # Expected sales volume estimation
        base_volume = 100
        expected_sales_volume = int(base_volume * demand_factor * (average_competitor_price / product.current_price))

        # Profit margin calculation
        cost_price = product.current_price * 0.7  # Assuming 70% of current price is cost
        profit_margin = ((recommended_price - cost_price) / recommended_price) * 100
        profit_margin = round(profit_margin, 2)

        logger.info(f"Optimized price for {product.product_id}: {recommended_price}")

        return OptimizePriceResponse(
            product_id=product.product_id,
            recommended_price=recommended_price,
            expected_sales_volume=expected_sales_volume,
            profit_margin=profit_margin
        )
    except Exception as e:
        logger.error(f"Error calculating recommended price for {product.product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during price calculation.")

# Endpoints
@app.post("/optimize_price", response_model=OptimizePriceResponse, summary="Optimize price for a single product")
async def optimize_price(product: ProductData):
    """
    Optimize the price for a single product based on current data.
    """
    return calculate_recommended_price(product)

@app.post("/bulk_optimize", response_model=BulkOptimizeResponse, summary="Optimize prices for multiple products")
async def bulk_optimize(request: BulkOptimizeRequest):
    """
    Optimize prices for multiple products in a single request.
    """
    try:
        recommendations = [calculate_recommended_price(product) for product in request.products]
        return BulkOptimizeResponse(recommendations=recommendations)
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail="Invalid input data.")
    except Exception as e:
        logger.error(f"Error during bulk optimization: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during bulk optimization.")

# Exception Handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

if __name__ == "__main__":
    uvicorn.run("price_pulse_api:app", host="0.0.0.0", port=8000, reload=True)
