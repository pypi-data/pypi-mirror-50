#! /usr/bin/env python3

import argparse
import sys
import json
from clint.textui import puts
from spag.helpers import game, configure


class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(0, '%s: error: %s\n' % (self.prog, message))


def main():
    parser = MyArgumentParser(description="Get information from the Giant Bomb API")

    subparsers = parser.add_subparsers(help='commands', dest="command")

    subparsers.add_parser("configure", help="Configure for your API key ")
    parser_search = subparsers.add_parser("search", help="Search for games")
    parser_search.add_argument("-n", "--name", help="Fuzzy Search of the name", action="store")
    parser_game = subparsers.add_parser("game", help="Search for a specific game")
    parser_game.add_argument("-g", "--guid", help="GUID of the exact game", action="store", required=True)
    parser_game.add_argument("-d", "--dlc", help="Additional DLC info", action="store_true")

    args = parser.parse_args()

    if args.command == "configure":
        return puts(json.dumps(configure.update_api_key(), indent=4))
    if args.command == "search":
        return puts(json.dumps(game.get_games(args), indent=4))
    if args.command == "game":
        return puts(json.dumps(game.get_game(args), indent=4))
    else:
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()