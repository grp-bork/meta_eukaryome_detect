# Output

## Output files

`run` writes its results to `<out_dir>/<sample_name>_metaeuk_output/`:

| File | Content |
|---|---|
| `readcounts.tsv` | Read statistics reported by ngless for the quality trimming step |
| `<reference>.depth_summary.tsv.gz` | One row per detected reference sequence (one file per reference) |
| `<reference>_filtered.bam` | Alignments that passed the identity and length filter, before the MAPQ filter |

`<reference>` is one of `pr2`, `mito`, `plastid`, `virulence` and `viruses`.

If nothing is detected for a reference, its depth summary contains only the header line.

## Depth summary columns

### Columns in every file

| Column | Description |
|---|---|
| `sample_name` | Sample name (`-s`, or the input directory name) |
| `ref_id` | ID of the reference sequence |
| `ref_length` | Length of the reference sequence (bp) |
| `avgdepth_cov` | Mean read depth over the covered positions |
| `breadth_cov` | Number of positions covered by at least one read |
| `breadth_fraction` | `breadth_cov` / `ref_length` |

See [Method](method.md#4-coverage-summary) for how these are computed.

### `pr2`

| Column | Description |
|---|---|
| `reference_type` | `protist` for the 18S sequences that are reported as detections, `competitive_mapper` for the rest of PR2 (see the note below) |
| `gene_cluster_id` | Numeric ID of the sequence (each PR2 sequence is its own cluster) |

The `ref_id` contains the PR2 taxonomy, separated by `|`. For example:
`JX948126.1.910_U|18S_rRNA|nucleus||Eukaryota|Alveolata|Apicomplexa|...|Cryptosporidium1_parvum`.

!!! note "competitive_mapper sequences"
    Reads are mapped against the whole of PR2, not only the protist targets, so that a read from a
    related organism maps to its own 18S sequence instead of being forced onto a target. Hits to
    `competitive_mapper` sequences are therefore expected. Filter on `reference_type == protist`
    to keep only the target protists.

### `mito` and `plastid`

| Column | Description |
|---|---|
| `ani_cluster_id` | Cluster of near-identical genomes this genome belongs to (`MTclstr_*` for mitochondria, `PLclstr_*` for plastids) |
| `full_taxonomy` | Taxonomy lineage, separated by `_` |
| `bin_names_in_cluster` | Species names of all genomes in the cluster, separated by `;` |
| `organism_groups_all` | Broad organism group, e.g. `Eukaryota;Plants;Land Plants` |
| `eukaryote_type1` | Ecological role, e.g. `food`, `symbiont`, `food/parasite` |
| `eukaryote_type2` | Finer category, e.g. `plant`, `commensal`, `pathogen` |
| `eukaryote_type3` | Food or role category, e.g. `Vegetables`, `Berries`, `Symbiont/fermented food` |
| `short_name` | Common name |
| `possible_contaminant_in_human_gut` | `1` or `2`: very likely a contaminant in human gut samples; `0`: not flagged |
| `other_notes` | Free-text notes, e.g. `Can be poisonous`, `Wine production` |

The annotation columns (`eukaryote_type*` to `other_notes`) are only filled in for some genomes and
are empty for the rest.

### `virulence`

| Column | Description |
|---|---|
| `gene_cluster_id` | ID of the cluster of near-identical virulence genes this gene belongs to |
| `SpName_x` | Description of the virulence factor and the genomes it is found in |

### `viruses`

These columns come from the NCBI Virus record of the genome.

| Column | Description |
|---|---|
| `Species` | Virus species |
| `Genus` | Virus genus |
| `Family` | Virus family |
| `Molecule_type` | Genome type, e.g. `dsDNA`, `ssRNA(+)` |
| `Host` | Host the virus was isolated from |
| `Isolation_Source` | Isolation source |
| `Collection_Date` | Collection date |
| `BioSample` | NCBI BioSample accession |
| `GenBank_Title` | GenBank record title |

## Interpreting the results

!!! tip "Breadth matters more than depth"
    A high `avgdepth_cov` with a low `breadth_fraction` means many reads pile up on a short part of
    the reference, for example a conserved region or a repeat. That is weak evidence that the
    organism is present. Reads from a genome that is really in the sample spread across it, so look
    for a high `breadth_fraction` first.

!!! tip "Clusters"
    Near-identical mitochondrial and plastid genomes and virulence genes are grouped into
    clusters (`ani_cluster_id`, `gene_cluster_id`). Reads from one organism can be shared between sequences of the same
    cluster, so sum or compare per cluster rather than per sequence.
