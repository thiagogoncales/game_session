#!/bin/bash -e

docker run -d -p 2345:8000 tray/dynamodb-local -port 8000 > /dev/null

# Wait until the docker container is available; retry maximum 2 times
echo "Health check on DynamoDB local docker container"
n=0
until [ $n -ge 2 ]
do
    echo "Connecting to DynamoDB local docker container..."
    aws dynamodb list-tables --endpoint-url http://localhost:2345 >/dev/null && break
    n=$[$n+1]
    sleep 2
    echo "Failed. Retry $n"
done

if [ $n -ge 2 ]
then
    echo "Unable to start DynamoDB local docker container"
    exit 1
fi
