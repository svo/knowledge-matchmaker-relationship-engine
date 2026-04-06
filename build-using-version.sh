#!/usr/bin/env bash

image=$1 &&
version=$2 &&
architecture=$3 &&

if [ -z "$architecture" ]; then
  docker run --rm -v "$(pwd)":/working-dir -v /var/run/docker.sock:/var/run/docker.sock --entrypoint ./bin/create-image-using-version svanosselaer/knowledge-matchmaker-relationship-engine-builder:latest "${image}" "${version}"
else
  docker run --rm -v "$(pwd)":/working-dir -v /var/run/docker.sock:/var/run/docker.sock --entrypoint ./bin/create-image-using-version "svanosselaer/knowledge-matchmaker-relationship-engine-builder:${architecture}" "${image}" "${version}" "${architecture}"
fi
