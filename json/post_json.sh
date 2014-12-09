curl 'http://localhost:8983/solr/update/json?commit=true' --data-binary @ieee_papers.json -H 'Content-type:text/json'
curl 'http://localhost:8983/solr/update/json?commit=true' --data-binary @acm_papers.json -H 'Content-type:text/json'
curl 'http://localhost:8983/solr/update/json?commit=true' --data-binary @other_ieee.json -H 'Content-type:text/json'
