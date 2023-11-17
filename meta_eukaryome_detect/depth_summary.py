#!/usr/bin/env python3
import gzip
from pathlib import Path

import pandas as pd

output_col_order = {
    'plastid': [
        "sample_name",
        "ref_id",
        "ref_length",
        "avgdepth_cov",
        "breadth_cov",
        "breadth_fraction",
        "ani_cluster_id",
        "full_taxonomy",
        "bin_names_in_cluster",
        "organism_groups_all",
    ],
    'mito': [
        "sample_name",
        "ref_id",
        "ref_length",
        "avgdepth_cov",
        "breadth_cov",
        "breadth_fraction",
        "ani_cluster_id",
        "full_taxonomy",
        "bin_names_in_cluster",
        "organism_groups_all",
    ],
    'pr2': [
        "sample_name",
        "ref_d",
        "breadth_cov",
        "gene_cluster_id",
        "ref_length",
        "breadth_fraction",
        "avg_depth_coverage",
    ],
    'virulence': [
        "ref_id",
        "breadth_cov",
        "gene_cluster_id",
        "SpName_x",
        "ref_length",
        "breadth_fraction",
        "sample_name",
        "avg_depth_coverage",
    ],
    'viruses': [
        "breadth_cov",
        "ref_id",
        "ref_length",
        "breadth_fraction",
        "sample_name",
        "avg_depth_coverage",
        "Species",
        "Genus",
        "Family",
        "Molecule_type",
        "Host",
        "Isolation_Source",
        "Collection_Date",
        "BioSample",
        "GenBank_Title",
    ],
}

breadth_coverages = {'plastid': 500, 'mito': 500, 'pr2': 100, 'virulence': 50, 'viruses': 100}

metadata_files = {
    'plastid': 'mito_plastid_metadata',
    'mito': 'mito_plastid_metadata',
    'pr2': 'pr2_metadata',
    'virulence': 'virulence_metadata',
    'viruses': 'viruses_metadata',
}


def get_depth_summary(out_dir: Path, reference: str, depth_file: Path, DB: Path):
    depths = pd.read_csv(depth_file, sep="\t", header=None, usecols=[0, 2], names=["ref_id", "depth_coverage"])
    out_file = out_dir / f"{reference}.depth_summary.tsv.gz"
    if len(depths) != 0:
        output = depths.groupby("ref_id").mean().rename(columns={"depth_coverage": "avg_depth_coverage"})
        output["breadth_cov"] = depths.groupby("ref_id").count()
        output = output[output["breadth_cov"] > breadth_coverages[reference]].sort_values(
            by="breadth_cov", ascending=False
        )

        contigLen = pd.read_csv(
            DB / metadata_files[reference],
            sep="\t",
            header=0,
        )
        output = pd.merge(output, contigLen, how="left", left_index=True, right_on=["ref_id"])

        output["breadth_fraction"] = output["breadth_cov"] / output["ref_length"]
        output["sample_name"] = 'test_sample'  # TODO this is temp
        output[output_col_order[reference]].round(4).to_csv(out_file, sep="\t", index=False, compression="gzip")

    else:
        with gzip.open(out_file, "wb") as f:
            f.write("\t".join(output_col_order[reference]).encode())
