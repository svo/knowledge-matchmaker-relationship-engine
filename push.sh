#!/usr/bin/env bash

image=$1 &&
architecture=$2 &&

if [ -z "$architecture" ]; then
  docker push "svanosselaer/knowledge-matchmaker-relationship-engine-${image}" --all-tags
else
  docker push "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:${architecture}"
fi
