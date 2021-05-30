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
ADA	74.16
BCH	0.00
BTC	43.42
DOGE	93.35
DOT	0.00
EOS	0.00
ETH	127.53
LINK	0.00
LTC	0.82
USDT	30.34
XLM	0.00
XRP	5.21
Unused	144.30
Total	519.12
```

### Buy currency

```
cx buy BTC 50
```

### Sell currency

```
cx sell BTC 50
```
