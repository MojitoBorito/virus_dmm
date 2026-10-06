out_50=/home/mojito/Desktop/BA/base/data/no_human/top_50
out_100=/home/mojito/Desktop/BA/base/data/no_human/top_100
out_same=/home/mojito/Desktop/BA/base/data/no_human/same_n

hvidb=/home/mojito/Desktop/BA/base/data/hvidb.tsv
intact=/home/mojito/Desktop/BA/base/data/intact.tsv
ppi=/home/mojito/Desktop/BA/base/data/string_700.tsv

# top50
mkdir -p $out_50
mkdir -p $out_50/corona
mkdir -p $out_50/hsv
mkdir -p $out_50/hiv

./intact_filter.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/corona --top_interactors 50 --suffix top_50.human_int --add_virus 
./intact_filter.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hsv --top_interactors 50 --suffix top_50.human_int --add_virus
./intact_filter.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hiv --top_interactors 50 --suffix top_50.human_int --add_virus

#top100
mkdir -p $out_100
mkdir -p $out_100/corona
mkdir -p $out_100/hsv
mkdir -p $out_100/hiv

./intact_filter.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/corona --top_interactors 100 --suffix top_100.human_int --add_virus
./intact_filter.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hsv --top_interactors 100 --suffix top_100.human_int --add_virus
./intact_filter.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hiv --top_interactors 100 --suffix top_100.human_int --add_virus

#same_n
mkdir -p $out_same
mkdir -p $out_same/corona
mkdir -p $out_same/hsv
mkdir -p $out_same/hiv
./intact_filter.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/corona --same --suffix same_n.human_int --add_virus
./intact_filter.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/hsv --same --suffix same_n.human_int --add_virus
./intact_filter.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/hiv --same --suffix same_n.human_int --add_virus