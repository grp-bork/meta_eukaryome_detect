import os
import sys


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


def get_ngless_filtering_template(reference_type):
    if reference_type == 'preprocess':
        return """
ngless "1.1"
import "mocat" version "0.0"
input = load_mocat_sample(ARGV[1])

input = preprocess(input, keep_singles=True) using |read|:
    read = smoothtrim(read, min_quality=20, window=4)
    if len(read) < 70:
        discard

write(input, ofile='preprocessed/preprocessed.fq' )
"""
    else:
        min_identity_pc = get_min_identity_pc(reference_type)
        return f"""
ngless "1.1"
import "parallel" version "1.0"
import "mocat" version "0.0"
import "samtools" version "0.0"

input = load_mocat_sample(ARGV[1])

mapped = map(input, fafile='${{2}}')
write(samtools_sort(mapped), ofile='unfiltered.bam' )

mapped = select(mapped) using |mr|:
    mr = mr.filter(min_match_size=70, min_identity_pc={min_identity_pc}, action={{drop}})
write(samtools_sort(mapped), ofile='filtered.bam' )
"""


def write_templates(out_dir):
    for template in ['preprocess', 'plastid', 'mito', 'pr2', 'virulence', 'viruses']:
        out_file = os.path.join(out_dir, template + '.ngless')
        with open(out_file, 'w') as f:
            f.write(get_ngless_filtering_template(template))
