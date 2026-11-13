# Database

The database is downloaded with `eukscan download_db` (see
[Installation](installation.md#download-the-database)). It holds five references, each with a BWA
0.7.17 index and a metadata table.

| Reference | Sequences | Content |
|---|---|---|
| `pr2` | 33,626 18S rRNA sequences (654 protist targets) | PR2 18S rRNA gene sequences |
| `mito` | 11,879 genomes | Eukaryotic mitochondrial genomes |
| `plastid` | 6,145 genomes | Plastid (chloroplast) genomes |
| `virulence` | 11,349 genes | Bacterial virulence factor genes |
| `viruses` | 13,582 genomes | NCBI Virus RefSeq genomes |

## PR2 18S rRNA

33,626 18S rRNA gene sequences from the [PR2](https://pr2-database.org/) database.

654 sequences are marked `protist`; these are the detection targets: mostly Apicomplexa
(e.g. *Cryptosporidium*), Discoba, Opalozoa, Conosa and Metamonada. The rest of PR2 is kept as
`competitive_mapper` sequences, so that reads from other eukaryotes, and from bacterial and
plastid 16S sequences in PR2, map to their own sequence instead of a target.

!!! warning "TODO"
    PR2 version; how the 654 protist targets were chosen.

## Mitochondria and plastids

11,879 mitochondrial and 6,145 plastid genomes, grouped by ANI into 11,932 clusters
(`ani_cluster_id`). Most are from land plants, fishes, insects and other animals, mammals, birds
and fungi.

About 2,900 genomes are annotated with their role in or near the human gut (food, symbiont,
parasite, ...); see the `mito` and `plastid` columns on the [Output](output.md#mito-and-plastid)
page.

!!! warning "TODO"
    Source and download date of the genomes (e.g. NCBI Organelle RefSeq); ANI threshold used for
    the clusters; who curated the annotation columns and how.

## Virulence factors

11,349 bacterial virulence factor genes, grouped into 6,683 gene clusters.

!!! warning "TODO"
    Source and version (the IDs are PATRIC `fig|` IDs, so possibly PATRIC_VF); clustering identity.

## Viruses

13,582 viral genomes from NCBI Virus RefSeq, released up to February 2021. The metadata comes from
NCBI Virus.

!!! warning "TODO"
    Download date and any filtering applied.
