# Database

The database is downloaded with `meta_eukaryome_detect download_db` (see
[Installation](installation.md#download-the-database)). It holds five references, each with a BWA
0.7.17 index and a metadata table. It is archived on Zenodo:
[10.5281/zenodo.24198236](https://doi.org/10.5281/zenodo.24198236).

| Reference | Sequences | Content |
|---|---|---|
| `pr2` | 33,626 18S rRNA sequences (654 protist targets) | PR2 18S rRNA gene sequences |
| `mito` | 11,879 genomes | Eukaryotic mitochondrial genomes |
| `plastid` | 6,145 genomes | Plastid (chloroplast) genomes |
| `virulence` | 11,349 genes | Bacterial virulence factor genes |
| `viruses` | 13,582 genomes | NCBI Virus RefSeq genomes |

## PR2 18S rRNA

33,626 16S and 18S rRNA gene sequences from the [PR2](https://pr2-database.org/) database
(v4.14), dereplicated with CD-HIT v4.7 from 197,602 sequences:

```
cd-hit-est -n 9 -c 0.97 -aS 0.5 -d 0 -r 1 -g 1 -M 30000 -sc 1
```

654 sequences are marked `protist`; these are the detection targets: mostly Apicomplexa
(e.g. *Cryptosporidium*), Discoba, Opalozoa, Conosa and Metamonada. The rest of PR2 is kept as
`competitive_mapper` sequences, so that reads from other eukaryotes, and from bacterial and
plastid 16S sequences in PR2, map to their own sequence instead of a target.

The targets cover 346 known human and animal eukaryotic symbionts that have no sequenced organelle
genome or no mitochondria, plus *Blastocystis*, which has many 18S rRNA reference sequences in
PR2. The database construction follows the approach of
[MARES](https://doi.org/10.1038/s41597-020-0549-9).

## Mitochondria and plastids

11,879 mitochondrial and 6,145 plastid genomes downloaded from NCBI GenBank on 25 January 2021,
covering 16,737 species and strains with names in NCBI Taxonomy. The genomes were compared
all-against-all with fastANI:

```
fastANI --refList <genomes> --ql <genomes> --matrix --minFraction 0.1 --fragLen 1000 -t 50 -o <out>
```

and grouped into 11,932 species clusters (`ani_cluster_id`) at 96% ANI for mitochondria and 98%
ANI for plastids. Most are from land plants, fishes, insects and other animals, mammals, birds
and fungi.

About 2,900 genomes are annotated with their role in or near the human gut (food, symbiont,
parasite, ...); see the `mito` and `plastid` columns on the [Output](output.md#mito-and-plastid)
page.

Highly prevalent species and known components of diet, pathogens and parasites were annotated by
hand. Pathogens follow the definitions of Jochum and Stecher (2020), and the lists of pathogenic and
commensal protozoa and fungi were curated from CDC and WHO documentation.

## Virulence factors

11,349 bacterial virulence factor genes, grouped into 6,683 gene clusters.

!!! warning "TODO"
    Source and version (the IDs are PATRIC `fig|` IDs, so possibly PATRIC_VF); clustering identity.

## Viruses

13,582 viral genomes from NCBI Virus RefSeq, released up to February 2021. The metadata comes from
NCBI Virus. No ANI thresholds were applied to the viral genomes.
