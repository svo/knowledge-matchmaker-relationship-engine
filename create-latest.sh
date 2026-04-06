#!/usr/bin/env bash

image=$1

docker manifest rm "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:latest" 2>/dev/null || true

docker manifest create \
  "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:latest" \
  --amend "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:amd64" \
  --amend "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:arm64" &&
docker manifest push "svanosselaer/knowledge-matchmaker-relationship-engine-${image}:latest"
