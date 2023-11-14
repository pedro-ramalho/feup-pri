curl -X POST -H 'Content-Type: application/json' --data-binary @schemas/species_schema.json http://localhost:8983/solr/species/schema

curl -X POST -H 'Content-Type: application/json' --data-binary @schemas/observations_schema.json http://localhost:8983/solr/observations/schema

curl -X POST -H 'Content-Type: application/json' --data-binary @schemas/images_schema.json http://localhost:8983/solr/images/schema

curl -X POST -H 'Content-Type: application/json' --data-binary @schemas/summary_abstracts_schema.json http://localhost:8983/solr/summary-abstracts/schema