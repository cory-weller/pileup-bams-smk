import sys
import os
from pathlib import Path

configfile: 'config.yaml'


bam_files = []

for i in config['bam_dirs']:
    bam_files += [x for x in Path(i).glob('*' + config['bam_suffix'])]

all_IDs = []
dir_dict = {}
for i in bam_files:
    base_name = i.name.rstrip(config['bam_suffix'])
    dir_dict[base_name] = i
    all_IDs.append(base_name)

print(all_IDs)
print(dir_dict)

localrules: count

rule all:
    input: expand('COUNTS/{sample_id}.counts.txt', sample_id=all_IDs)

rule count:
    input: bamfile = lambda wildcards: dir_dict[wildcards.sample_id]
    output: countsfile = temp('COUNTS/' + '{sample_id}.counts.txt')
    envmodules: 'samtools/1.23'
    params:
        variantsfile = config['variantsfile'],
    script: 'parse.py'
