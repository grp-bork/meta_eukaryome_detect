# meta_eukaryome_detect

![metaEukaryome](assets/logo-horizontal.svg){ .logo-light width="360" }
![metaEukaryome](assets/logo-horizontal-on-dark.svg){ .logo-dark width="360" }

[![pypi](https://img.shields.io/pypi/v/meta_eukaryome_detect.svg)](https://pypi.org/project/meta_eukaryome_detect/)
[![bioconda](https://img.shields.io/conda/vn/bioconda/meta_eukaryome_detect.svg)](https://anaconda.org/bioconda/meta_eukaryome_detect)
[![downloads](https://img.shields.io/conda/dn/bioconda/meta_eukaryome_detect.svg)](https://anaconda.org/bioconda/meta_eukaryome_detect)
[![licence](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pathogen, Parasite, Eukaryote and Virus detection in metagenomes.

meta_eukaryome_detect is the package for **metaEukaryome**, which detects eukaryotes, viruses and
virulence genes in metagenomes. It installs the `meta_eukaryome_detect` command and `eukscan`, a
shorter alias of it.

## metaEukaryome

metaEukaryome takes the short reads of a metagenomic sample and maps them against five
curated references to report which eukaryotes, viruses and virulence genes are present, and how
well each reference sequence is covered.

| Reference | Detects |
|---|---|
| `pr2` | Eukaryotes (protists) via their 18S rRNA gene, from the [PR2](https://pr2-database.org/) database |
| `mito` | Eukaryotes via their mitochondrial genomes |
| `plastid` | Eukaryotes (mostly plants and algae) via their plastid genomes |
| `virulence` | Bacterial virulence factor genes |
| `viruses` | Viruses (NCBI Virus RefSeq genomes) |

## How it works

```
reads ─► quality trimming ─► map to each reference ─► identity / length filter ─► MAPQ filter ─► per-base depth ─► coverage summary
         (ngless)            (ngless, bwa)             (ngless)                     (samtools)     (samtools)
```

Each reference has its own identity, mapping-quality and coverage thresholds.
See [Method](method.md) for the details.

## Quick start

```bash
conda install -c bioconda meta_eukaryome_detect
meta_eukaryome_detect download_db /path/to/db_dir
meta_eukaryome_detect run -i /path/to/sample_dir -d /path/to/db_dir -t 16 -p
```

The results are written to `<sample_name>_metaeuk_output/`. See [Output](output.md) for what each file
and column means.

## Links

* Source code: <https://github.com/grp-bork/meta_eukaryome_detect>
* PyPI: <https://pypi.org/project/meta_eukaryome_detect/>
* Bioconda: <https://anaconda.org/bioconda/meta_eukaryome_detect>
* Free software: MIT
