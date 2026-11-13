# Installation

## Requirements

* Python ≥ 3.11
* [ngless](https://ngless.embl.de/) (≥ 1.1)
* [samtools](https://www.htslib.org/)
* About 3 GB of disk space for the database

## Install

=== "Bioconda (recommended)"

    Installs meta_eukaryome_detect together with ngless and samtools.

    ```bash
    conda install -c bioconda -c conda-forge meta_eukaryome_detect
    ```

=== "pip"

    pip only installs the Python package. `ngless` and `samtools` must be installed separately
    and be available on your `PATH`.

    ```bash
    pip install meta_eukaryome_detect
    ```

=== "Containers"

    Docker and Singularity images are built automatically by BioContainers from the bioconda
    package: <https://biocontainers.pro/tools/meta_eukaryome_detect>

Check that the installation worked:

```bash
meta_eukaryome_detect -h
```

`eukscan` is a shorter alias and can be used in place of `meta_eukaryome_detect` everywhere.

## Download the database

The database has to be downloaded once before the first run:

```bash
meta_eukaryome_detect download_db /path/to/db_dir
```

The target directory must already exist. The download is about 1.4 GB compressed and about 3 GB
once decompressed. Each file is checked against its MD5 sum, and a failed file is downloaded again
up to 3 times.

The directory then contains, for each of the five references (`pr2`, `mito`, `plastid`,
`virulence`, `viruses`):

* `<reference>_reference`: the reference sequences (FASTA)
* `<reference>_reference-bwa-0.7.17.*`: the BWA index used by ngless
* a metadata table used to annotate the results (`pr2_metadata`, `mito_plastid_metadata`,
  `virulence_metadata`, `viruses_metadata`)

See [Database](database.md) for what each reference contains.

### Pointing `run` at the database

Either pass the directory on every run:

```bash
meta_eukaryome_detect run -d /path/to/db_dir ...
```

or set it once as an environment variable:

```bash
export META_EUKARYOME_DETECT_DB_DIR=/path/to/db_dir
```
