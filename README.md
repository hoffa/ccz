# cx

Intuitive cryptocurrency trading.

All prices are in a fixed quote currency.

## Setup

Create a `config.json` with the exchange configuration:

```json
{
  "exchange": "ndax",
  "quote": "CAD",
  "auth": {
    "apiKey": "a1b2c3d4e5f6",
    "secret": "f6e5d4c3b2a1"
  }
}
```

## Trading

### Show balance

``` bash
cx balance
```

```
BTC     43.09219863
LTC     0.8148226559999999
ETH     128.95158
XRP     5.210472
BCH     0.0
CAD     163.987874994
EOS     0.0
XLM     0.0
DOGE    73.896626568
ADA     72.277920468
USDT    30.336705
LINK    0.0
DOT     0.0
Total   518.568200316
```

### Buy currency

```
cx buy BTC 50
```

### Sell currency

```
cx sell BTC 50
```
