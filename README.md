# Korea Economic Indicators API

Real-time South Korea economic data including GDP, inflation, unemployment, and interest rates. Powered by World Bank Open Data.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All economic indicators snapshot |
| `GET /gdp` | GDP (current USD) |
| `GET /growth` | GDP growth rate (annual %) |
| `GET /gdp-per-capita` | GDP per capita (current USD) |
| `GET /inflation` | Inflation rate — CPI (annual %) |
| `GET /unemployment` | Unemployment rate |
| `GET /interest-rate` | Lending interest rate |
| `GET /current-account` | Current account balance |

## Data Source

World Bank Open Data
https://data.worldbank.org/country/KR

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
