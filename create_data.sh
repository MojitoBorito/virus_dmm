#!/bin/bash
mkdir -p data/out_corona_intact_filter
mkdir -p data/out_corona_hvidb_filter
mkdir -p data/out_hsv_intact_filter
mkdir -p data/out_hsv_hvidb_filter
mkdir -p data/out_hiv_intact_filter
mkdir -p data/out_hiv_hvidb_filter
./virfil.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir data/out_corona_intact_filter --percentile 0.95
./virfil.py --tax_id 2697049 --database_name hvidb --database_file data/hvidb.tsv --human_file data/string_700.tsv --output_dir data/out_corona_hvidb_filter --percentile 0.95
./virfil.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir data/out_hsv_intact_filter --percentile 0.95
./virfil.py --tax_id 10298 --database_name hvidb --database_file data/hvidb.tsv --human_file data/string_700.tsv --output_dir data/out_hsv_hvidb_filter --percentile 0.95
./virfil.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir data/out_hiv_intact_filter --percentile 0.95
./virfil.py --tax_id 11676 --database_name hvidb --database_file data/hvidb.tsv --human_file data/string_700.tsv --output_dir data/out_hiv_hvidb_filter --percentile 0.95