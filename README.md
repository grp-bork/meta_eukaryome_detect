# meta_eukaryome_detect

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/grp-bork/meta_eukaryome_detect/main/docs/assets/logo-horizontal-on-dark.svg">
  <img alt="metaEukaryome" src="https://raw.githubusercontent.com/grp-bork/meta_eukaryome_detect/main/docs/assets/logo-horizontal.svg" width="360">
</picture>


[![pypi](https://img.shields.io/pypi/v/meta_eukaryome_detect.svg)](https://pypi.org/project/meta_eukaryome_detect/)
[![bioconda](https://img.shields.io/conda/vn/bioconda/meta_eukaryome_detect.svg)](https://anaconda.org/bioconda/meta_eukaryome_detect)
[![licence](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Pathogen, Parasite, Eukaryote and Virus detection in metagenomes.

meta_eukaryome_detect is the package for **metaEukaryome**, which detects eukaryotes, viruses and
virulence genes in metagenomes. It maps the reads of a metagenomic sample against five references (PR2 18S rRNA,
mitochondrial genomes, plastid genomes, bacterial virulence factors and viral genomes) and reports
the coverage of each reference sequence detected.

## Quick start

```bash
conda install -c bioconda meta_eukaryome_detect
meta_eukaryome_detect download_db /path/to/db_dir
meta_eukaryome_detect run -i /path/to/sample_dir -d /path/to/db_dir -t 16 -p
```

`eukscan` is a shorter alias of the `meta_eukaryome_detect` command.

* Documentation: <https://grp-bork.embl-community.io/grp-microbiome-astrology/meta_eukaryome_detect/>
* GitHub: <https://github.com/grp-bork/meta_eukaryome_detect>
* PyPI: <https://pypi.org/project/meta_eukaryome_detect/>
* Free software: MIT
