#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path


def check_if_tool_exists(tool_name):
    """Check if tool is available."""
    return shutil.which(tool_name) is not None


def ngless(template: Path, cpu_count: str, temp_dir: Path, sample_folder: Path, verbose: bool, DB_path='') -> None:
    """Run ngless.

    Arguments:
        template (str): full path of gene calls
        threads (int): number of threads to use
        temp_dir (str): path of directory to use for tmp files
        database_file (str): full path fof diamond db file
        out_file (str): full path of output file
    """
    if verbose:
        ngless_verbosity = '--trace'
    else:
        ngless_verbosity = ''
    try:
        subprocess.check_output(
            [
                "ngless",
                "--temporary-directory",
                temp_dir,
                template,
                "--jobs",
                cpu_count,
                sample_folder,
                ngless_verbosity,
                DB_path,
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Failed to run ngless on {sample_folder} \n {e.output}")


def samtools_unique(filtered_bam: Path, unique_bam: Path, verbose: bool) -> None:
    """Run samtools.

    Arguments:

    """
    try:
        subprocess.check_output(
            [
                "samtools",
                "view",
                "-bq",
                '1',
                filtered_bam,
                "-o",
                unique_bam,
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Failed to run samtools view on {filtered_bam} \n {e.output}")


def samtools_depth(unique_bam: Path, unique_depth: Path, verbose: bool) -> None:
    """Run samtools.

    Arguments:

    """
    try:
        subprocess.check_output(
            [
                "samtools",
                "depth",
                unique_bam,
                "-o",
                unique_depth,
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Failed to run samtools view on {unique_bam} \n {e.output}")
