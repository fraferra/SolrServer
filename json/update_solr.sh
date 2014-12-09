for f in `ls papers/ `; do
  pdf2txt.py -t text -o results/test.txt "papers/$f"
  python update_to_solr.py results/test.txt

done