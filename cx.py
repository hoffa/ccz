#!/usr/bin/env python3

import argparse
from argparse import Namespace
import json

import ccxt  # type: ignore

from dataclasses import dataclass
from typing import cast, Dict, List


@dataclass
class Ticker:
    bid: float
    ask: float


class Client:
    def __init__(self, exchange: str, auth: Dict[str, str]) -> None:
        self.client = getattr(ccxt, exchange)(auth)

    def get_balance(self) -> Dict[str, float]:
        return cast(Dict[str, float], self.client.fetch_balance()["free"])

    def get_symbols(self) -> List[str]:
        self.client.load_markets()
        return cast(List[str], self.client.symbols)

    def get_ticker(self, symbol: str) -> Ticker:
        ticker = self.client.fetch_ticker(symbol)
        return Ticker(ticker["bid"], ticker["ask"])

    def buy(self, symbol: str, amount: float) -> None:
        self.client.create_market_buy_order(symbol, amount)

    def sell(self, symbol: str, amount: float) -> None:
        self.client.create_market_sell_order(symbol, amount)


def print_float(x: float) -> None:
    print(f"{x:.6f}")


def command_balance(client: Client, args: Namespace) -> None:
    for currency, amount in client.get_balance().items():
        print(f"{currency}\t{amount}")


def command_symbols(client: Client, args: Namespace) -> None:
    for symbol in client.get_symbols():
        print(symbol)


def command_buy(client: Client, args: Namespace) -> None:
    client.buy(args.symbol, args.amount)


def command_sell(client: Client, args: Namespace) -> None:
    client.sell(args.symbol, args.amount)


def command_bid(client: Client, args: Namespace) -> None:
    ticker = client.get_ticker(args.symbol)
    print_float(ticker.bid)


def command_ask(client: Client, args: Namespace) -> None:
    ticker = client.get_ticker(args.symbol)
    print_float(ticker.ask)


def command_price(client: Client, args: Namespace) -> None:
    ticker = client.get_ticker(args.symbol)
    price = ticker.bid if args.side == "bid" else ticker.ask
    if args.direction == "base":
        print_float(args.amount / price)
    else:
        print_float(args.amount * price)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    subparsers = parser.add_subparsers()

    parser_balance = subparsers.add_parser("balance")
    parser_balance.set_defaults(func=command_balance)

    parser_symbols = subparsers.add_parser("symbols")
    parser_symbols.set_defaults(func=command_symbols)

    parser_buy = subparsers.add_parser("buy")
    parser_buy.add_argument("symbol")
    parser_buy.add_argument("amount", type=float)
    parser_buy.set_defaults(func=command_buy)

    parser_sell = subparsers.add_parser("sell")
    parser_sell.add_argument("symbol")
    parser_sell.add_argument("amount", type=float)
    parser_sell.set_defaults(func=command_sell)

    parser_ask = subparsers.add_parser("ask")
    parser_ask.add_argument("symbol")
    parser_ask.set_defaults(func=command_ask)

    parser_bid = subparsers.add_parser("bid")
    parser_bid.add_argument("symbol")
    parser_bid.set_defaults(func=command_bid)

    parser_price = subparsers.add_parser("price")
    parser_price.add_argument("direction", choices=("base", "quote"))
    parser_price.add_argument("side", choices=("bid", "ask"))
    parser_price.add_argument("symbol")
    parser_price.add_argument("amount", type=float)
    parser_price.set_defaults(func=command_price)

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    client = Client(config["exchange"], config["auth"])

    args.func(client, args)


if __name__ == "__main__":
    main()
