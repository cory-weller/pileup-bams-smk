#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


# Function to quickly print a list as tab-separated values
def tabsep(mylist):
    return'\t'.join([str(x) for x in mylist])

def check_index(filename):
    '''
    Checks for .bam.bai index, generates it if needed.
    '''
    index_file = Path(filename + '.bai')
    if not index_file.exists():
        mycmd = f'samtools index {filename}'.split()
        subprocess.run(mycmd)

def get_variant_counts(bamfile, variantfile):
    mycmd = f'samtools mpileup -l {variantfile} {bamfile}'.split()
    pileup = subprocess.check_output(mycmd).decode().strip().split('\n')
    result = ''
    for line in pileup:
        try:
            chr, pos, c3, c4, c5, c6 = line.split('\t')
            base_A = len([x for x in c5 if x in ['a','A']])
            base_C = len([x for x in c5 if x in ['c','C']])
            base_T = len([x for x in c5 if x in ['t','T']])
            base_G = len([x for x in c5 if x in ['g','G']])
            result += tabsep([snakemake.wildcards.sample_id, chr, pos, base_A, base_C, base_T, base_G]) + '\n'
        except:
            print(f'bad line:\n{line}')
    return result

check_index(snakemake.input.bamfile)
allele_counts = get_variant_counts(snakemake.input.bamfile, snakemake.params.variantsfile)

header = tabsep(['sample_id','chr','pos','A','C','T','G'])

with open(snakemake.output.countsfile, 'w') as outfile:
    outfile.write(header + '\n')
    outfile.write(allele_counts)
