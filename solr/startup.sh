#!/bin/bash

docker run -p 8983:8983 --name fungi_solr -v ${PWD}/data:/data -d solr:9.3

sleep 1

# create cores
docker exec -it fungi_solr solr create_core -c species
docker exec -it fungi_solr solr create_core -c observations
docker exec -it fungi_solr solr create_core -c images
docker exec -it fungi_solr solr create_core -c summary-abstracts

# upload schema
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/schemas/species_schema.json http://localhost:8983/solr/species/schema
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/schemas/observations_schema.json http://localhost:8983/solr/observations/schema
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/schemas/images_schema.json http://localhost:8983/solr/images/schema
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/schemas/summary_abstracts_schema.json http://localhost:8983/solr/summary-abstracts/schema

# populate collections
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/data/species.json http://localhost:8983/solr/species/update?commit=true
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/data/observations.json http://localhost:8983/solr/observations/update?commit=true
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/data/images.json http://localhost:8983/solr/images/update?commit=true
curl -X POST -H 'Content-Type: application/json' --data-binary @solr/data/summary-abstracts.json http://localhost:8983/solr/summary-abstracts/update?commit=true
