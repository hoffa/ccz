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
  "exchange": "binance",
  "quote": "cad",
  "auth": {
    "apiKey": "foo",
    "secret": "bar"
  }
}
```

`exchange` is the exchange ID as defined by [CCXT](https://github.com/ccxt/ccxt). See [CCXT docs](https://github.com/ccxt/ccxt/wiki/Manual#api-keys-setup) for `auth` structure.

## Trading

### Show balance

```bash
cx balance
```

```
ada     74.11
bch     0.00
btc     43.71
doge    94.06
dot     0.00
eos     0.00
eth     127.98
link    0.00
ltc     0.82
usdt    20.34
xlm     0.00
xrp     5.22
unused  154.27
total   520.51
```

### Buy currency

```
cx buy btc 50
```

### Sell currency

```
cx sell btc 50
```
