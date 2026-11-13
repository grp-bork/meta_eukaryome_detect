# Usage

`eukscan` has two subcommands:

* `download_db`: download the reference database (see [Installation](installation.md#download-the-database))
* `run`: analyse one metagenomic sample

## Input

`run` analyses one sample at a time. A sample is a directory holding that sample's FASTQ files.
The directory is read with ngless'
[`load_mocat_sample`](https://ngless.embl.de/Functions.html#load-mocat-sample), so files are
grouped into pairs and singles by their suffix:

```
sample_A/
├── run1_1.fq.gz       # forward reads
├── run1_2.fq.gz       # reverse reads
└── run1.single.fq.gz  # unpaired reads (optional)
```

Several runs or lanes of the same sample can sit in the same directory; they are all used. See the
ngless documentation for the full list of accepted suffixes.

By default, the output files are named after the directory (`sample_A` above). Use `-s` to choose
another name.

## Running a sample

```bash
eukscan run \
    -i /path/to/sample_A \
    -d /path/to/db_dir \
    -o /path/to/results \
    -t 16 -p
```

This creates `/path/to/results/sample_A_metaeuk_output/`. See [Output](output.md).

### Options

| Option | Default | Description |
|---|---|---|
| `-i`, `--input_sample_dir` | (required) | Directory with the sample's FASTQ files |
| `-d`, `--db_dir` | `$META_EUKARYOME_DETECT_DB_DIR` | Database directory |
| `-s`, `--sample_name` | name of input dir | Name used for output files and the `sample_name` column |
| `-o`, `--out_dir` | current directory | Where the output directory is created. Must already exist |
| `-t`, `--threads` | 4 | Number of CPU threads |
| `-p`, `--parallel` | off | Map against the references in parallel (see below) |
| `--temp_dir` | `--out_dir` | Where the temporary directory is created |
| `--keep_temp_files` | off | Keep the temporary directory after the run |
| `-v`, `--verbose` | off | Debug logging, and ngless runs with `--trace` |

Advanced options set the minimum mapping quality (MAPQ) for each reference; see
[Method](method.md#filters-per-reference) for why the defaults differ:

| Option | Default |
|---|---|
| `--min_map_qual_pr2` | 20 |
| `--min_map_qual_plastid` | 1 |
| `--min_map_qual_mito` | 1 |
| `--min_map_qual_virulence` | 20 |
| `--min_map_qual_virus` | 0 |

### Threads and `--parallel`

Without `--parallel`, the five references are mapped one after another, each using all `-t`
threads.

With `--parallel`, the references are mapped at the same time and the threads are split between
them. This only takes effect with more than 7 threads:

| `-t` | Mappings at once | Threads per mapping |
|---|---|---|
| ≤ 7 | 1 | `-t` |
| 8–20 | `-t` / 4 | `-t` / number at once |
| > 20 | 5 | `-t` / 5 |

Quality trimming always runs first, on all threads.

### Temporary files

Trimmed reads and intermediate BAM and depth files are written to
`<temp_dir>/<sample_name>_ngless_temp_dir/`. The directory is deleted at the end of the run unless
`--keep_temp_files` is given. It holds a full copy of the trimmed reads, so point `--temp_dir` at
fast local scratch space with room for that.

## Running many samples

Each run handles one sample. For many samples, loop over the sample directories:

```bash
for sample in /path/to/samples/*/; do
    eukscan run -i "$sample" -d /path/to/db_dir -o /path/to/results -t 16 -p
done
```

or, on a SLURM cluster, submit one job per sample as an array:

```bash
#!/bin/bash
#SBATCH --array=1-100
#SBATCH --cpus-per-task=16
sample=$(sed -n "${SLURM_ARRAY_TASK_ID}p" samples.txt)
eukscan run -i "$sample" -d /path/to/db_dir -o /path/to/results \
    -t "$SLURM_CPUS_PER_TASK" -p --temp_dir "$TMPDIR"
```

where `samples.txt` lists one sample directory per line.

To combine the results, concatenate the `<reference>.depth_summary.tsv.gz` files of all samples.
Every row carries a `sample_name` column, so rows from different samples stay distinguishable.
