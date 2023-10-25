#!/usr/bin/env python3

import argparse
from command.predict import execute as predict_command
from command.save import execute as save_command
from command.list import execute as list_command


def main():
    parser = argparse.ArgumentParser(
        description="when: A menstrual cycle prediction tool for lll",
        add_help=False,
        prog="when",
    )

    parser.add_argument(
        "-p",
        "--predict",
        metavar="DATE",
        type=str,
        help="Predict the next menstrual period date and duration based on past data.",
    )
    parser.add_argument(
        "-s",
        "--save",
        nargs=2,
        metavar=("START_DATE", "END_DATE"),
        type=str,
        help="Save menstrual period data.",
    )
    parser.add_argument(
        "-l",
        "--list",
        metavar="NUM_RECORDS",
        type=int,
        nargs="?",
        const=-1,
        help="List last menstrual records. Optionally limit by number of records.",
    )
    parser.add_argument(
        "-h", "--help", action="store_true", help="Display this help message."
    )

    args = parser.parse_args()

    command_args = {
        "predict": args.predict,
        "save": args.save,
        "list": args.list,
    }

    commands = {
        "predict": predict_command,
        "save": save_command,
        "list": list_command,
    }

    if args.help:
        parser.print_help()
        return

    executed = False
    for cmd, arg in command_args.items():
        if arg != None:
            commands[cmd](arg)
            executed = True
            break

    if not executed:
        parser.print_help()


if __name__ == "__main__":
    main()
