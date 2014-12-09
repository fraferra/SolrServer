for f in `ls papers/ `; do
  pdf2txt.py -t text -o test.txt $f
  python 2json.py results/test.txt
  curl 'http://localhost:8983/solr/update/json?commit=true' --data-binary @output.json -H 'Content-type:text/json'
done


