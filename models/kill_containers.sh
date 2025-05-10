#!/bin/bash

# Usage: ./kill-matching-containers.sh "<regex>"
# Example: ./kill-matching-containers.sh "myapp.*"

if [ -z "$1" ]; then
  echo "Usage: $0 <regex>"
  exit 1
fi

REGEX="$1"

# Get list of running container IDs and names
docker ps --format "{{.ID}} {{.Names}}" | while read -r id name; do
  if [[ $name =~ $REGEX ]]; then
    echo "Killing container: $name ($id)"
    docker kill "$id"
  fi
done