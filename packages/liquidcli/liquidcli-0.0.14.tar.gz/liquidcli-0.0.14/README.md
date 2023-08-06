# liquid-python

[![CircleCI](https://circleci.com/gh/suzuito/liquid-python.svg?style=svg)](https://circleci.com/gh/suzuito/liquid-python)

Client library for [Liquid](https://www.liquid.com/).
Liquid API reference is [here](https://developers.liquid.com).

<details><summary>Supported API</summary>
<p>

|End point|Impl|Unit test|
|---|----|----|
|Public|||
|`GET /products/`|||
|`GET /products/:id`|||
|`GET /products/:id/price_levels`|||
|`GET /executions`|o||
|`GET /ir_ladders`|||
|`GET /fees`|||
|Private|||
|`POST /orders`|||
|`GET /orders/:id`|||
|`GET /orders`|||
|`PUT /orders/:id/cancel`|||
|`PUT /orders/:id`|||
|`GET /orders/:id/trades`|||
|`GET /executions/me`|||
|`GET /fiat_accounts`|||
|`POST /fiat_accounts`|||
|`GET /crypto_accounts`|||
|`GET /accounts/balance`|||
|`GET /accounts/:currency`|||
|`GET /accounts/:currency/reserved_balance_details`|||
|`POST /loan_bids`|||
|`GET /loan_bids`|||
|`PUT /loan_bids/:id/close`|||
|`GET /loans`|||
|`PUT /loans`|||
|`GET /trading_accounts`|||
|`GET /trading_accounts/:id`|||
|`GET /trades`|||
|`PUT /trades/:id/close`|||
|`PUT /trades/close_all`|||
|`PUT /trades/:id/adjust_margin`|||
|`GET /trades/:id/loans`|||
|...etc...|||

</p></details>

## Usage

### Insatall

```bash
pip install liquid-python
```

### Run

```bash
# Execute unit test
pipenv run python -m pytest --cov=liquidcli --cov-report=html --cov-report=term ./tests
# Check coverage in HTML
open htmlcov/index.html
```

## Development

```bash
# Installation of dependencies
pipenv install --dev
# Run
pipenv python run main.py
```

## Contribution

TBD