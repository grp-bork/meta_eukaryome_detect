#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from datetime import datetime

from . import external_tools, meta_eukaryome_database

logger = logging.getLogger("meta_eukaryome_detect.py")


def parse_args(args):
    """Parse Arguments

    Arguments:
        args (List): List of args supplied to script.

    Returns:
        Namespace: assigned args

    """
    description = "Pathogen, Parasite, Eukaryote and Virus detection in metagenomes.\n"

    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(title="meta_eukaryome_detect subcommands", metavar="", dest="cmd")
    run = subparsers.add_parser("run", help="Run Meta-Eukaryome-Detection.")
    download_db = subparsers.add_parser("download_db", help="Download meta_eukaryome_detect db.")
    run.add_argument(
        "-r",
        "--db_file",
        help="meta_eukaryome_database directory. Default: META_EUKARYOME_DETECT_DB envvar",
        default=os.environ.get("META_EUKARYOME_DETECT_DB"),
        metavar="",
    )
    run.add_argument(
        "-v",
        "--verbose",
        help="Verbose output for debugging",
        action="store_true",
        default=False,
    )
    download_db.add_argument("path", help="Download database to given direcory.", metavar="dest_path")
    if not args:
        parser.print_help(sys.stderr)
        sys.exit(1)
    download_db.add_argument(
        "-v",
        "--verbose",
        help="Verbose output for debugging",
        action="store_true",
        default=False,
    )
    args = parser.parse_args(args)
    return args


def start_checks():
    """Checks if tool dependencies are available."""
    if not external_tools.check_if_tool_exists("diamond"):
        logger.error("Diamond 2.0.4 not found.")
        sys.exit(1)
    else:
        diamond_ver = external_tools.check_diamond_version()
        if diamond_ver != "2.0.4":
            logger.error(f"Diamond version is {diamond_ver}, not 2.0.4")
            sys.exit(1)
    if not external_tools.check_if_tool_exists("ngless"):
        logger.error("Ngless not found.")
        sys.exit(1)
    if not external_tools.check_if_tool_exists("grep"):
        logger.error("grep not found.")
        sys.exit(1)
    if not external_tools.check_if_tool_exists("zcat"):
        logger.error("zcat not found.")
        sys.exit(1)


def main():
    args = parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(
            format="%(asctime)s : [%(levelname)7s] : %(name)s:%(lineno)s %(funcName)20s() : %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            format="%(asctime)s : %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
    logger = logging.getLogger("meta_eukaryome_detect.py")
    logger.debug(args)
    start_time = datetime.now()
    logger.info(f'START {start_time.strftime("%Y-%m-%d")}')
    if args.cmd == "download_db":
        meta_eukaryome_database.get_db(args.path)
    if args.cmd == "run":
        start_checks()
        if not args.db_file:
            logger.error("Database_file argument missing.")
            sys.exit(1)
        else:
            if not os.path.isfile(args.db_file):
                logger.error("Database_file not found.")
                sys.exit(1)

        # run(args)


if __name__ == "__main__":
    main()
