The recommended method of installation is through [bioconda](https://anaconda.org/bioconda/meta_eukaryome_detect)

    $ conda install -c bioconda meta_eukaryome_detect

## Download meta_eukaryome_detect DB

Before use the meta_eukaryome_detect DB needs to be downloaded::

    $ meta_eukaryome_detect download_db /path/to/output/dir/

The path to the META_EUKARYOME_DETECT_DB_DIR can be supplied as a command line argument
to :code:`meta_eukaryome_detect run` or set as an environment variable: :code:`META_EUKARYOME_DETECT_DB_DIR`

## Manual Installation

Alternatively meta_eukaryome_detect can be install using pip::

    $ pip install meta_eukaryome_detect

META_EUKARYOME_DETECT_DB should be downloaded by following the above instructions.
Separately dependencies `ngless` and `samtools` need to be installed


## Containers

Both Singularity and docker containers are available by following instructions here: [LINK](https://biocontainers.pro/#/tools/meta_eukaryome_detect)
