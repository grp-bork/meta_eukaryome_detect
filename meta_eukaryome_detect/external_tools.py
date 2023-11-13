#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path


def check_if_tool_exists(tool_name):
    """Check if tool is available."""
    return shutil.which(tool_name) is not None


def ngless(template: Path, cpu_count: str, temp_dir: Path, sample_folder: Path) -> None:
    """Run ngless.

    Arguments:
        template (str): full path of gene calls
        threads (int): number of threads to use
        temp_dir (str): path of directory to use for tmp files
        database_file (str): full path fof diamond db file
        out_file (str): full path of output file
    """
    try:
        subprocess.check_output(
            [
                "ngless",
                "--temporary-directory",
                temp_dir,
                "--jobs",
                cpu_count,
                template,
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Failed to run ngless on {sample_folder} \n {e.output}")
