from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from datetime import datetime

app = FastAPI(
    title="Korea Economic Indicators API",
    description="Real-time South Korea economic data including GDP, inflation, unemployment, and interest rates. Powered by World Bank Open Data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/KR/indicator"

INDICATORS = {
    "gdp":            {"id": "NY.GDP.MKTP.CD",    "name": "GDP",                          "unit": "Current USD"},
    "gdp_growth":     {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP Growth Rate",              "unit": "Annual %"},
    "gdp_per_capita": {"id": "NY.GDP.PCAP.CD",    "name": "GDP Per Capita",               "unit": "Current USD"},
    "inflation":      {"id": "FP.CPI.TOTL.ZG",   "name": "Inflation (CPI)",              "unit": "Annual %"},
    "unemployment":   {"id": "SL.UEM.TOTL.ZS",   "name": "Unemployment Rate",            "unit": "% of Labor Force"},
    "lending_rate":   {"id": "FR.INR.LEND",       "name": "Lending Interest Rate",        "unit": "%"},
    "current_acct":   {"id": "BN.CAB.XOKA.CD",   "name": "Current Account Balance",      "unit": "Current USD"},
    "gni":            {"id": "NY.GNP.MKTP.CD",    "name": "Gross National Income",        "unit": "Current USD"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {
        "format": "json",
        "mrv": limit,
        "per_page": limit,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url, params=params)
        data = res.json()

    if not data or len(data) < 2:
        return []

    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Korea Economic Indicators API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "World Bank Open Data",
        "country": "Korea, Republic of (KR)",
        "endpoints": ["/summary", "/gdp", "/growth", "/gdp-per-capita", "/inflation", "/unemployment", "/interest-rate", "/current-account"],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=5, ge=1, le=30)):
    """All key South Korea economic indicators snapshot"""
    tasks = {key: fetch_wb(meta["id"], limit) for key, meta in INDICATORS.items()}
    results = {}
    for key, coro in tasks.items():
        results[key] = await coro
    formatted = {
        key: {
            "name": INDICATORS[key]["name"],
            "unit": INDICATORS[key]["unit"],
            "data": results[key],
        }
        for key in INDICATORS
    }
    return {
        "country": "Korea, Republic of",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": formatted,
    }


@app.get("/gdp")
async def gdp(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea GDP (current USD)"""
    data = await fetch_wb("NY.GDP.MKTP.CD", limit)
    return {
        "indicator": "GDP",
        "series_id": "NY.GDP.MKTP.CD",
        "unit": "Current USD",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/growth")
async def gdp_growth(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea GDP growth rate (annual %)"""
    data = await fetch_wb("NY.GDP.MKTP.KD.ZG", limit)
    return {
        "indicator": "GDP Growth Rate",
        "series_id": "NY.GDP.MKTP.KD.ZG",
        "unit": "Annual %",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/gdp-per-capita")
async def gdp_per_capita(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea GDP per capita (current USD)"""
    data = await fetch_wb("NY.GDP.PCAP.CD", limit)
    return {
        "indicator": "GDP Per Capita",
        "series_id": "NY.GDP.PCAP.CD",
        "unit": "Current USD",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/inflation")
async def inflation(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea inflation rate — Consumer Price Index (annual %)"""
    data = await fetch_wb("FP.CPI.TOTL.ZG", limit)
    return {
        "indicator": "Inflation, Consumer Prices",
        "series_id": "FP.CPI.TOTL.ZG",
        "unit": "Annual %",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/unemployment")
async def unemployment(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea unemployment rate (% of labor force)"""
    data = await fetch_wb("SL.UEM.TOTL.ZS", limit)
    return {
        "indicator": "Unemployment Rate",
        "series_id": "SL.UEM.TOTL.ZS",
        "unit": "% of Labor Force",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/interest-rate")
async def interest_rate(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea lending interest rate (%)"""
    data = await fetch_wb("FR.INR.LEND", limit)
    return {
        "indicator": "Lending Interest Rate",
        "series_id": "FR.INR.LEND",
        "unit": "%",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/current-account")
async def current_account(limit: int = Query(default=10, ge=1, le=60)):
    """South Korea current account balance (BoP, current USD)"""
    data = await fetch_wb("BN.CAB.XOKA.CD", limit)
    return {
        "indicator": "Current Account Balance",
        "series_id": "BN.CAB.XOKA.CD",
        "unit": "Current USD (Balance of Payments)",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }
