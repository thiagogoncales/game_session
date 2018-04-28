#!/bin/bash -e

# get_physical_resource_id ${stack-name} ${logical-resource-id}
get_docker_container_id() {
    echo $(docker ps -a -q --filter ancestor=$1 --format="{{.ID}}")
}

DYNAMO_CONTAINERS=$(get_docker_container_id "tray/dynamodb-local")
docker stop ${DYNAMO_CONTAINERS} >> /dev/null
