#!/usr/bin/env python3
import gzip
import hashlib
import logging
import os
import shutil
import sys

import requests


def md5sum_file(file):
    """Computes MD5 sum of file.

    Arguments:
        file (str): Path of file to md5sum

    Returns:
        str: md5sum
    """
    block_size = 8192
    m = hashlib.md5()
    with open(file, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                return m.hexdigest()
            m.update(data)


def download_file(file_url, out_file):
    """Download a file to disk

    Streams a file from URL to disk.

    Arguments:
        file_url (str): URL of file to download
        out_file (str): Target file path
    """
    with requests.get(file_url, stream=True) as r:
        with open(out_file, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def decompress_gzip_file(gz_file, out_file):
    """Decompress a gzip file.

    Uncompressed given gzip file to out_file.

    Arguments:
        gz_file (str): Path of gzip file
        out_file (str): Path of target uncompressed out file
    """
    with gzip.open(gz_file, "rb") as f_in:
        with open(out_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_md5_file(file_url):
    """Read md5sums from url

    Arguments:
        file_url (str): URL of file

    Returns:
        dict: {file: md5sum}
    """
    md5s = requests.get(f"{file_url}").text.split("\n")
    return {x.split('  ')[1]: x.split('  ')[0] for x in md5s if x}


def check_md5(expected_md5, file_path):
    """Check md5 and remove file if incorect.

    Arguments:
        expected_md5 (str): Expected md5 of file
        file_path (str): Path of file
    """
    downloaded_md5 = md5sum_file(file_path)
    if downloaded_md5 != expected_md5:
        os.unlink(file_path)
        return False
    else:
        return True


def get_db(base_dir):
    """Download GUNC DB.

    Arguments:
        base_dir (str): Path of output directory
    """
    logging.basicConfig(
        format="%(asctime)s : %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    if not os.path.isdir(base_dir):
        sys.exit(f"[ERROR] Output Directory {base_dir} doesnt exist.")
    base_url = "https://swifter.embl.de/~fullam/meta_eukaryome_database/"
    files_to_download = get_md5_file(f"{base_url}MD5SUM_gzipped")
    uncompressed_md5s = get_md5_file(f"{base_url}MD5SUM")
    count_files_to_download = len(files_to_download)
    logger.info("[INFO] DB downloading...")
    for i, file_name in enumerate(files_to_download, 1):
        logger.info(f"[INFO] Downloading {i}/{count_files_to_download} {file_name}")
        gz_file_url = f"{base_url}{file_name}"
        gz_file_path = os.path.join(base_dir, file_name)
        out_file = gz_file_path.replace(".gz", "")
        out_file_name = file_name.replace(".gz", "")

        retry = 3
        while retry:
            download_file(gz_file_url, gz_file_path)
            if not check_md5(files_to_download[file_name], gz_file_path):
                logger.error(f"[ERROR] MD5 check failed, removing {gz_file_path}")
                retry -= 1
                continue
            decompress_gzip_file(gz_file_path, out_file)
            if not check_md5(uncompressed_md5s[out_file_name], out_file):
                logger.error(f"[ERROR] MD5 check failed, removing {out_file}")
                retry -= 1
                continue
            else:
                break
        else:
            if retry == 0:
                sys.exit('Downloading database files failed too many times')
        os.unlink(gz_file_path)

    logger.info("[INFO] DB download successful.")
    logger.info(f"[INFO] DB path: {os.path.abspath(base_dir)}")
