#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from . import create_ngless_template, external_tools, meta_eukaryome_database

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
        "-d",
        "--db_file",
        help="meta_eukaryome_database directory. Default: META_EUKARYOME_DETECT_DB envvar",
        default=os.environ.get("META_EUKARYOME_DETECT_DB"),
        metavar="",
    )
    run.add_argument(
        "-o",
        "--out_dir",
        help="Output dir.  Default: cwd",
        default=os.getcwd(),
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


def create_dir(path):
    """Create a directory

    Will create a directory if it doesnt already exist.

    Arguments:
        path (str): directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def start_checks(args):
    """Checks if tool dependencies are available."""
    if not external_tools.check_if_tool_exists("ngless"):
        logger.error("Ngless not found.")
        sys.exit(1)
    if not os.path.isdir(args.out_dir):
        logger.error(f"Output Directory {args.out_dir} doesnt exist.")
        sys.exit(1)


def run(args):
    ngless_template_dir = Path(args.out_dir) / 'ngless_templates'
    create_dir(ngless_template_dir)
    create_ngless_template.write_templates(ngless_template_dir)


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
        start_checks(args)
        if not args.db_file:
            logger.error("Database_file argument missing.")
            sys.exit(1)
        else:
            if not os.path.isdir(args.db_file):
                logger.error("Database_file not found.")
                sys.exit(1)

        run(args)


if __name__ == "__main__":
    main()
