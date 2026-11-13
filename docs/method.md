# Method

## 1. Quality trimming

All reads in the sample directory are trimmed with ngless `smoothtrim` (minimum quality 20, window
size 4). Reads shorter than 70 bp after trimming are discarded; a read whose mate is discarded is
kept as a single. The read statistics ngless reports for this step are copied to `readcounts.tsv`.

## 2. Mapping

The trimmed reads are mapped separately against each of the five references with ngless `map`,
which uses BWA-MEM. Each mapping keeps only alignments of at least 70 bp with at least the
reference's minimum identity (table below). These alignments are written to
`<reference>_filtered.bam`.

## 3. Mapping quality filter

The filtered alignments are further restricted to those with a mapping quality of at least the
reference's minimum MAPQ (`samtools view -q`).

A low MAPQ means a read maps equally well to several reference sequences. For `pr2` and
`virulence`, where many sequences are near-identical, a MAPQ of 20 removes reads that cannot be
assigned to one sequence. The `mito` and `plastid` defaults only remove reads with MAPQ 0. The
`viruses` default keeps all reads.

## 4. Coverage summary

`samtools depth` reports the depth at each covered position of each reference sequence. For each
sequence, this gives:

* `breadth_cov`: the number of positions covered by at least one read
* `avgdepth_cov`: the mean depth over those covered positions (positions with no reads are not
  counted)
* `breadth_fraction`: `breadth_cov` / `ref_length`, the fraction of the sequence that is covered

Only sequences with `breadth_cov` above the reference's threshold are reported. The rows are
annotated from the reference's metadata table and sorted by `breadth_cov`, highest first.

## Filters per reference

| Reference | Min. identity | Min. alignment length | Default min. MAPQ | Reported if `breadth_cov` > |
|---|---|---|---|---|
| `pr2` | 97% | 70 bp | 20 | 100 bp |
| `mito` | 96% | 70 bp | 1 | 500 bp |
| `plastid` | 98% | 70 bp | 1 | 500 bp |
| `virulence` | 95% | 70 bp | 20 | 50 bp |
| `viruses` | 95% | 70 bp | 0 | 100 bp |

The identity, alignment length and breadth thresholds are fixed. The MAPQ thresholds can be changed
with the `--min_map_qual_*` options (see [Usage](usage.md#options)).
