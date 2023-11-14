curl -X POST -H 'Content-Type: application/json' --data-binary @data/species.json http://localhost:8983/solr/species/update?commit=true

curl -X POST -H 'Content-Type: application/json' --data-binary @data/observations.json http://localhost:8983/solr/observations/update?commit=true

curl -X POST -H 'Content-Type: application/json' --data-binary @data/images.json http://localhost:8983/solr/images/update?commit=true

curl -X POST -H 'Content-Type: application/json' --data-binary @data/summary-abstracts.json http://localhost:8983/solr/summary-abstracts/update?commit=true
