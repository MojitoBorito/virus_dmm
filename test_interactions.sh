out_50=/home/mojito/Desktop/BA/base/data/interactions_top_50
out_100=/home/mojito/Desktop/BA/base/data/interactions_top_100

hvidb=/home/mojito/Desktop/BA/base/data/hvidb.tsv
intact=/home/mojito/Desktop/BA/base/data/intact.tsv
ppi=/home/mojito/Desktop/BA/base/data/string_700.tsv

# top50
mkdir -p $out_50
mkdir -p $out_50/corona
mkdir -p $out_50/hsv
mkdir -p $out_50/hiv

./intact_filter.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/corona --top_interactions 50
./intact_filter.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hsv --top_interactions 50
./intact_filter.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hiv --top_interactions 50

#top100
mkdir -p $out_100
mkdir -p $out_100/corona
mkdir -p $out_100/hsv
mkdir -p $out_100/hiv

./intact_filter.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/corona --top_interactions 100
./intact_filter.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hsv --top_interactions 100
./intact_filter.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hiv --top_interactions 100