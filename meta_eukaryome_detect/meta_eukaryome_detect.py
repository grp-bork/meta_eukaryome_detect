#!/usr/bin/env python3
import argparse
import logging
import multiprocessing
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from . import create_ngless_template, depth_summary, external_tools, meta_eukaryome_database

logger = logging.getLogger("meta_eukaryome_detect.py")


def parse_args(args):
    """Parse Arguments

    Arguments:
        args: List of args supplied to script.

    Returns:
        Namespace: assigned args

    """
    description = "Pathogen, Parasite, Eukaryote and Virus detection in metagenomes.\n"
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=155)
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)
    subparsers = parser.add_subparsers(title="meta_eukaryome_detect subcommands", metavar="", dest="cmd")
    run = subparsers.add_parser("run", help="Run Meta-Eukaryome-Detection.", formatter_class=formatter)
    run_group = run.add_mutually_exclusive_group(required=True)
    advanced_run = run.add_argument_group('Advanced Options')
    download_db = subparsers.add_parser(
        "download_db", help="Download meta_eukaryome_detect db.", formatter_class=formatter
    )
    run.add_argument(
        "-d",
        "--db_dir",
        help="meta_eukaryome_database directory. Default: META_EUKARYOME_DETECT_DB_DIR envvar",
        default=os.environ.get("META_EUKARYOME_DETECT_DB_DIR"),
        metavar="",
    )
    run_group.add_argument(
        "-i",
        "--input_sample_dir",
        help="""Input directory contining fasta files for a sample
             (suffixes of the form _1.fq.gz .2.fq.gz single.fg.gz allowed)""",
        metavar="",
    )
    run.add_argument(
        "-s",
        "--sample_name",
        help="Name to give to output files, Default: Name of input dir",
        default=None,
        metavar="",
    )
    advanced_run.add_argument(
        "--min_map_qual_plastid",
        help="Minimum Mapping quality to use for plastid reference.",
        default='1',
        metavar="",
    )
    advanced_run.add_argument(
        "--min_map_qual_mito",
        help="Minimum Mapping quality to use for mitochondria reference.",
        default='1',
        metavar="",
    )
    advanced_run.add_argument(
        "--min_map_qual_pr2",
        help="Minimum Mapping quality to use for pr2 reference.",
        default='20',
        metavar="",
    )
    advanced_run.add_argument(
        "--min_map_qual_virulence",
        help="Minimum Mapping quality to use for virulence reference.",
        default='20',
        metavar="",
    )
    advanced_run.add_argument(
        "--min_map_qual_virus",
        help="Minimum Mapping quality to use for virus reference.",
        default='0',
        metavar="",
    )
    run.add_argument(
        "-t",
        "--threads",
        help="number of CPU threads. Default: 4",
        default="4",
        metavar="",
    )
    run.add_argument(
        "-p",
        "--parallel",
        help="Run all mappings in parallel (threads will be split between each of the 5 references)",
        action="store_true",
        default=False,
    )
    run.add_argument(
        "-o",
        "--out_dir",
        help="Output dir.  Default: cwd",
        default=os.getcwd(),
        metavar="",
    )
    run.add_argument(
        "--temp_dir",
        help="Directory to store temp files. Default: cwd",
        default=None,
        metavar="",
    )
    run.add_argument(
        "--keep_temp_files",
        help="Do not remove temproary files",
        action="store_true",
        default=False,
    )
    run.add_argument(
        "-v",
        "--verbose",
        help="Verbose output for debugging",
        action="store_true",
        default=False,
    )
    download_db.add_argument("path", help="Download database to given directory.", metavar="dest_path")
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
        logger.debug(f'Creating dir: {path}')
        os.makedirs(path)


def start_checks(args):
    """Checks if tool dependencies are available."""
    if not external_tools.check_if_tool_exists("ngless"):
        logger.error("Ngless not found.")
        sys.exit(1)
    if not external_tools.check_if_tool_exists("samtools"):
        logger.error("Samtools not found.")
        sys.exit(1)
    if not os.path.isdir(args.out_dir):
        logger.error(f"Output Directory {args.out_dir} doesnt exist.")
        sys.exit(1)


def run(args):
    input_dir = Path(args.input_sample_dir)
    if not args.sample_name:
        sample_name = input_dir.name
    else:
        sample_name = args.sample_name

    if args.temp_dir:
        ngless_temp_dir = Path(args.temp_dir) / f'{sample_name}_ngless_temp_dir'
    else:
        ngless_temp_dir = Path(args.out_dir) / f'{sample_name}_ngless_temp_dir'

    create_dir(ngless_temp_dir)
    ngless_template_dir = ngless_temp_dir / 'ngless_templates'
    create_dir(ngless_template_dir)
    result_dir = Path(args.out_dir) / f'{sample_name}_metaeuk_output'
    create_dir(result_dir)
    templates = create_ngless_template.write_templates(ngless_template_dir, ngless_temp_dir, result_dir)
    logger.info('Running Preprocessing of input files.')
    logger.debug(f'Running template: {templates["preprocess"]}')
    preprocessed_temp_dir = ngless_temp_dir / 'preprocessed'
    create_dir(preprocessed_temp_dir)
    external_tools.ngless(templates['preprocess'], args.threads, preprocessed_temp_dir, input_dir, args.verbose)
    read_count_file = ngless_template_dir / 'preprocess.ngless.output_ngless' / 'fq.tsv'
    shutil.copyfile(read_count_file, result_dir / 'readcounts.tsv')
    mapping_qualities = {
        'plastid': args.min_map_qual_plastid,
        'mito': args.min_map_qual_mito,
        'pr2': args.min_map_qual_pr2,
        'virulence': args.min_map_qual_virulence,
        'viruses': args.min_map_qual_virus,
    }
    meta = []
    threads = int(args.threads)
    if threads > 7 and args.parallel:
        if threads < 21:
            jobs = int(threads / 4)
            threads = int(threads / jobs)
        else:
            jobs = 5
            threads = int(threads / jobs)
    else:
        jobs = 1
    for template in ['plastid', 'mito', 'pr2', 'virulence', 'viruses']:
        meta.append(
            (
                template,
                templates[template],
                mapping_qualities[template],
                args,
                str(threads),
                result_dir,
                ngless_temp_dir,
                sample_name,
            )
        )
    p = multiprocessing.Pool(jobs)
    p.map(run_detection, meta)
    if not args.keep_temp_files:
        shutil.rmtree(ngless_temp_dir)


def run_detection(meta):
    template, template_path, mapping_quality, args, threads, result_dir, ngless_temp_dir, sample_name = meta
    logger.debug(f'Running reference: {template} with args: {meta}')
    DB_path = Path(args.db_dir) / f'{template}_reference'
    logger.debug(f'DB Path: {DB_path}')
    external_tools.ngless(
        template_path,
        threads,
        ngless_temp_dir,
        ngless_temp_dir / 'preprocessed',
        args.verbose,
        DB_path,
    )
    unfiltered_bam = ngless_temp_dir / f"{template}_unfiltered.bam"
    filtered_bam = result_dir / f"{template}_filtered.bam"
    unique_bam = ngless_temp_dir / f"{template}_unique.bam"
    unique_depth = ngless_temp_dir / f"{template}_unique.depth"
    external_tools.samtools_unique(filtered_bam, unique_bam, mapping_quality, args.verbose)
    external_tools.samtools_depth(unique_bam, unique_depth, args.verbose)
    depth_summary.get_depth_summary(result_dir, template, unique_depth, Path(args.db_dir), sample_name)
    if not args.keep_temp_files:
        unfiltered_bam.unlink()
        # filtered_bam.unlink()
        unique_depth.unlink()
    logger.info(f'Finished running reference: {template}')


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
        if not args.db_dir:
            logger.error("Database_dir argument missing.")
            sys.exit(1)
        else:
            if not os.path.isdir(args.db_dir):
                logger.error("Database_dir not found.")
                sys.exit(1)
        run(args)
    end_time = datetime.now()
    logger.info(f'END {end_time.strftime("%Y-%m-%d")}')


if __name__ == "__main__":
    main()
