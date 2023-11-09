#!/bin/bash

#docker run -p 8983:8983 --name fungi_solr -v ${PWD}/solr-data:/data -d solr:9.3 solr-precreate fungi-data 
docker run -p 8983:8983 --name fungi_solr -v ${PWD}/data:/data -d solr:9.3
sleep 1
docker exec -it fungi_solr solr create_core -c species
docker exec -it fungi_solr solr create_core -c observations
docker exec -it fungi_solr solr create_core -c images
docker exec -it fungi_solr solr create_core -c summary-abstracts
