#!/usr/bin/env python3

import argparse
import json
import sys
from argparse import Namespace
from typing import Dict, Iterator, Tuple

import ccxt  # type: ignore


# TODO: Cache tickers
# TODO: buy-all
# TODO: sell-all
class Client:
    """Designed for intuitive fiat trading."""

    def __init__(self, exchange: str, auth: Dict[str, str], quote: str) -> None:
        self.client = getattr(ccxt, exchange)(auth)
        self.client.load_markets()
        self.quote = quote

    def _get_currencies(self) -> Iterator[str]:
        for symbol in self.client.symbols:
            base, quote = self.parse_symbol(symbol)
            if quote == self.quote:
                yield base

    def _get_ticker(self, symbol: str) -> Tuple[float, float]:
        ticker = self.client.fetch_ticker(symbol)
        return ticker["bid"], ticker["ask"]

    def get_balance(self) -> Iterator[Tuple[str, float]]:
        currencies = list(self._get_currencies())
        total = 0
        balance = self.client.fetch_balance()["free"]
        for currency, amount in sorted(balance.items()):
            if currency == self.quote:
                total += amount
            elif currency in currencies:
                symbol = self.get_symbol(currency)
                bid, _ = self._get_ticker(symbol)
                quote_amount = amount * bid
                yield currency, quote_amount
                total += quote_amount
        yield "Unused", balance[self.quote]
        yield "Total", total

    def buy(self, currency: str, amount: float) -> None:
        symbol = self.get_symbol(currency)
        _, ask = self._get_ticker(symbol)
        base_amount = amount / ask
        self.client.create_market_buy_order(symbol, base_amount)

    def sell(self, currency: str, amount: float) -> None:
        symbol = self.get_symbol(currency)
        bid, _ = self._get_ticker(symbol)
        base_amount = amount / bid
        self.client.create_market_sell_order(symbol, base_amount)

    @staticmethod
    def parse_symbol(symbol: str) -> Tuple[str, str]:
        base, quote = symbol.split("/")
        return base, quote

    def get_symbol(self, currency: str) -> str:
        return f"{currency}/{self.quote}"


def command_balance(client: Client, args: Namespace) -> None:
    for currency, amount in client.get_balance():
        print(f"{currency}\t{amount:.2f}")


def command_buy(client: Client, args: Namespace) -> None:
    client.buy(args.currency, args.amount)


def command_sell(client: Client, args: Namespace) -> None:
    client.sell(args.symbol, args.amount)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    subparsers = parser.add_subparsers(dest="cmd")

    parser_balance = subparsers.add_parser("balance")
    parser_balance.set_defaults(func=command_balance)

    parser_buy = subparsers.add_parser("buy")
    parser_buy.add_argument("currency")
    parser_buy.add_argument("amount", type=float)
    parser_buy.set_defaults(func=command_buy)

    parser_sell = subparsers.add_parser("sell")
    parser_sell.add_argument("symbol")
    parser_sell.add_argument("amount", type=float)
    parser_sell.set_defaults(func=command_sell)

    args = parser.parse_args()

    if not args.cmd:
        parser.print_usage()
        sys.exit(1)

    with open(args.config) as f:
        config = json.load(f)
    client = Client(config["exchange"], config["auth"], config["quote"])

    args.func(client, args)


if __name__ == "__main__":
    main()
