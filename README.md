# pileup-bams-smk


Edit `config.yaml`:
- `bam_suffix` indicates what string to strip off of the end of bam filenames. The remaining text is assumed to be the sample ID.
- `bam_dirs` indicates the directories to check for bam files.
- `variantsfile` points to a text file listing sites to count alleles. Defaults to `variants.txt` which can be edited to desired sites.

`sbatch run.sh` submits a single job that will iterate (serially) over all the bam files.

To run in parallel, remove `counts` from the `localrules` section of `snakefile`.