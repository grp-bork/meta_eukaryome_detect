#!/usr/bin/env python3
import shutil
import subprocess
import sys


def prodigal(input_file, out_file):
    """Run prodigal

    Arguments:
        input_file (str): full path of input fasta
        out_file (str): fullpath of output file
    """
    try:
        if input_file.endswith(".gz"):
            uncompressed = subprocess.Popen(("zcat", input_file), stdout=subprocess.PIPE)
            subprocess.check_output(
                [
                    "prodigal",
                    "-i",
                    "/dev/stdin",
                    "-a",
                    out_file,
                    "-o",
                    "/dev/null",
                    "-p",
                    "meta",
                    "-q",
                ],
                stdin=uncompressed.stdout,
                universal_newlines=True,
            )
        else:
            subprocess.check_output(
                [
                    "prodigal",
                    "-i",
                    input_file,
                    "-a",
                    out_file,
                    "-o",
                    "/dev/null",
                    "-p",
                    "meta",
                    "-q",
                ],
                universal_newlines=True,
            )
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to run Prodigal {input_file}")


def diamond(input_file, threads, temp_dir, database_file, out_file):
    """Run diamond.

    Arguments:
        input_file (str): full path of gene calls
        threads (int): number of threads to use
        temp_dir (str): path of directory to use for tmp files
        database_file (str): full path fof diamond db file
        out_file (str): full path of output file
    """
    try:
        subprocess.check_output(
            [
                "diamond",
                "blastp",
                "--query",
                input_file,
                "--threads",
                threads,
                "--max-target-seqs",
                "1",
                "--masking",
                "0",
                "--evalue",
                "1",
                "--algo",
                "0",
                "--tmpdir",
                temp_dir,
                "--db",
                database_file,
                "--out",
                out_file,
                "--quiet",
            ],
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] Failed to run Diamond on {input_file} \n {e.output}")


def check_diamond_version():
    """Return version of diamond found."""
    return subprocess.check_output("diamond --version", shell=True, universal_newlines=True).strip().split()[2]


def check_if_tool_exists(tool_name):
    """Check if tool is available."""
    return shutil.which(tool_name) is not None
