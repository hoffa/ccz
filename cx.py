#!/usr/bin/env python3

import argparse
import json

import ccxt


def get_symbol(base, quote):
    return f"{base}/{quote}".upper()


def print_float(x):
    print(f"{x:.6f}")


def command_balance(client, args):
    balance = client.fetch_balance()
    symbol = args.quote.upper()
    print(balance["total"][symbol])


def command_buy(client, args):
    symbol = get_symbol(args.base, args.quote)
    client.create_market_buy_order(symbol, args.amount)


def command_sell(client, args):
    symbol = get_symbol(args.base, args.quote)
    client.create_market_sell_order(symbol, args.amount)


def command_price(client, args):
    symbol = get_symbol(args.base, args.quote)
    ticker = client.fetch_ticker(symbol)
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
    parser_balance.add_argument("quote")
    parser_balance.set_defaults(func=command_balance)

    parser_buy = subparsers.add_parser("buy")
    parser_buy.add_argument("base")
    parser_buy.add_argument("quote")
    parser_buy.add_argument("amount", type=float)
    parser_buy.set_defaults(func=command_buy)

    parser_sell = subparsers.add_parser("sell")
    parser_sell.add_argument("base")
    parser_sell.add_argument("quote")
    parser_sell.add_argument("amount", type=float)
    parser_sell.set_defaults(func=command_sell)

    parser_price = subparsers.add_parser("price")
    parser_price.add_argument("direction", choices=("base", "quote"))
    parser_price.add_argument("side", choices=("bid", "ask"))
    parser_price.add_argument("base")
    parser_price.add_argument("quote")
    parser_price.add_argument("amount", type=float)
    parser_price.set_defaults(func=command_price)

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    client = getattr(ccxt, config["exchange"])(config["auth"])

    args.func(client, args)


if __name__ == "__main__":
    main()
