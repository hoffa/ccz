# cx

Intuitive cryptocurrency trading.

All prices are in a fixed quote currency.

## Installation

```bash
cd "$(mktemp -d)"
git clone https://github.com/hoffa/cx.git .
python3 setup.py install
```

## Setup

Create a `config.json` with the exchange configuration:

```json
{
  "exchange": "ndax",
  "quote": "CAD",
  "auth": {
    "apiKey": "foo",
    "secret": "bar"
  }
}
```

`exchange` is the exchange ID as defined by [CCXT](https://github.com/ccxt/ccxt). See [CCXT docs](https://github.com/ccxt/ccxt/wiki/Manual#api-keys-setup) for `auth` structure.

## Trading

### Show balance

``` bash
cx balance
```

```
BTC     43.02
LTC     0.81
ETH     127.01
XRP     5.24
BCH     0.00
CAD     163.99
EOS     0.00
XLM     0.00
DOGE    73.88
ADA     72.82
USDT    30.34
LINK    0.00
DOT     0.00
Total   517.11
```

### Buy currency

```
cx buy BTC 50
```

### Sell currency

```
cx sell BTC 50
```
