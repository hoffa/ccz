#!/usr/bin/env python3

import argparse
import json

import ccxt


def print_float(x):
    print(f"{x:.6f}")


def command_balance(client, _):
    balance = client.fetch_balance()
    for currency, amount in balance["free"].items():
        print(f"{currency}\t{amount}")


def command_symbols(client, _):
    client.load_markets()
    for symbol in client.symbols:
        print(symbol)


def command_buy(client, args):
    client.create_market_buy_order(args.symbol, args.amount)


def command_sell(client, args):
    client.create_market_sell_order(args.symbol, args.amount)


def command_bid(client, args):
    ticker = client.fetch_ticker(args.symbol)
    print_float(ticker["bid"])


def command_ask(client, args):
    ticker = client.fetch_ticker(args.symbol)
    print_float(ticker["ask"])


def command_price(client, args):
    ticker = client.fetch_ticker(args.symbol)
    price = ticker[args.side]
    if args.direction == "base":
        print_float(args.amount / price)
    else:
        print_float(args.amount * price)


def main():
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
    client = getattr(ccxt, config["exchange"])(config["auth"])

    args.func(client, args)


if __name__ == "__main__":
    main()
