

# find all _tagged.txt files and tar them up 
find . -name "*_tagged.txt" -exec tar -cvf tagged.tar {} \;

# find all .txt but not _tagged.txt files and tar them up
find . -name "*.txt" ! -name "*_tagged.txt" -exec tar -cvf /data/home/raul/miscosas/repos/mario_plumber/transform_tagged_or_txt_to_daedalus_vrt/videos/2020_txt.tar {} \;


# find all *_US_KMEX_*.txt or *_ES_*.txt files 
find . -name "*_US_KMEX_*.txt" -o -name "*_ES_*.txt" -exec tar -cvf /data/home/raul/miscosas/repos/mario_plumber/transform_tagged_or_txt_to_daedalus_vrt/videos/2020_txt.tar {} \;


# find all *.daedalus_vrt and append them to a single file
find . -name "*.daedalus_vrt" -exec cat {} \; >> /data/home/raul/miscosas/repos/mario_plumber/transform_tagged_or_txt_to_daedalus_vrt/videos/2020_daedalus_vrt.txt

