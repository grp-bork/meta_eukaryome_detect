
To use meta-eukaryome-detect

```
meta_eukaryome_detect -h
```
## Installation


The recommended method of installation is through [bioconda](https://anaconda.org/bioconda/meta-eukaryome-detect)

    $ conda install -c bioconda meta-eukaryome-detect

## Download meta-eukaryome-detect DB

Before use the meta-eukaryome-detect DB needs to be downloaded::

    $ meta-eukaryome-detect download_db /path/to/output/dir/

The path to the META_EUKARYOME_DETECT_DB_DIR can be supplied as a command line argument
to :code:`meta-eukaryome-detect run` or set as an environment variable: :code:`META_EUKARYOME_DETECT_DB_DIR`

## Manual Installation

Alternatively meta-eukaryome-detect can be install using pip::

    $ pip install meta-eukaryome-detect

META_EUKARYOME_DETECT_DB should be downloaded by following the above instructions.
Separately dependencies need to be installed


## Containers

Both Singularity and docker containers are available by following instructions here: [LINK](https://biocontainers.pro/#/tools/meta-eukaryome-detect)
