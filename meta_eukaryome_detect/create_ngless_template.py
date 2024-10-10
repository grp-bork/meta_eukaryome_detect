import sys
from pathlib import Path


def get_min_identity_pc(reference_type):
    match reference_type:
        case 'plastid':
            return '98'
        case 'mito':
            return '96'
        case 'pr2':
            return '97'
        case 'virulence':
            return '95'
        case 'viruses':
            return '95'
        case _:
            sys.exit(f'{reference_type} not a valid reference type!')


def get_ngless_filtering_template(reference_type: str, temp_dir: Path, result_dir: Path):
    if reference_type == 'preprocess':
        return f"""
ngless "1.1"
import "mocat" version "0.0"
input = load_mocat_sample(ARGV[1])

input = preprocess(input, keep_singles=True) using |read|:
    read = smoothtrim(read, min_quality=20, window=4)
    if len(read) < 70:
        discard

write(input, ofile='{temp_dir}/preprocessed/preprocessed.fq' )
"""
    else:
        min_identity_pc = get_min_identity_pc(reference_type)
        return f"""
ngless "1.1"
import "parallel" version "1.0"
import "mocat" version "0.0"
import "samtools" version "0.0"

input = load_mocat_sample(ARGV[1])

mapped = map(input, fafile=ARGV[2])
write(samtools_sort(mapped), ofile='{temp_dir}/{reference_type}_unfiltered.bam' )

mapped = select(mapped) using |mr|:
    mr = mr.filter(min_match_size=70, min_identity_pc={min_identity_pc}, action={{drop}})
write(samtools_sort(mapped), ofile='{result_dir}/{reference_type}_filtered.bam' )
"""


def write_templates(out_dir, temp_dir, result_dir):
    templates = {}
    for template in ['preprocess', 'plastid', 'mito', 'pr2', 'virulence', 'viruses']:
        out_file = Path(out_dir) / f'{template}.ngless'
        templates[template] = out_file
        with open(out_file, 'w') as f:
            f.write(get_ngless_filtering_template(template, temp_dir, result_dir))
    return templates
