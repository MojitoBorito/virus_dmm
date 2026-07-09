out_50=/home/mojito/Desktop/BA/base/data/top_50
out_100=/home/mojito/Desktop/BA/base/data/top_100
out_same=/home/mojito/Desktop/BA/base/data/same_n

hvidb=/home/mojito/Desktop/BA/base/data/hvidb.tsv
intact=/home/mojito/Desktop/BA/base/data/intact.tsv
ppi=/home/mojito/Desktop/BA/base/data/string_700.tsv

# top50
mkdir -p $out_50
mkdir -p $out_50/corona
mkdir -p $out_50/hsv
mkdir -p $out_50/hiv

./virfil.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/corona --top 50
./virfil.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hsv --top 50
./virfil.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_50/hiv --top 50

#top100
mkdir -p $out_100
mkdir -p $out_100/corona
mkdir -p $out_100/hsv
mkdir -p $out_100/hiv

./virfil.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/corona --top 100 
./virfil.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hsv --top 100
./virfil.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_100/hiv --top 100

#same_n
mkdir -p $out_same
mkdir -p $out_same/corona
mkdir -p $out_same/hsv
mkdir -p $out_same/hiv
./virfil.py --tax_id 2697049 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/corona --same
./virfil.py --tax_id 10298 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/hsv --same
./virfil.py --tax_id 11676 --database_name intact --database_file data/intact.tsv --human_file data/string_700.tsv --output_dir $out_same/hiv --same