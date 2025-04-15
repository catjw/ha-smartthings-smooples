#! /usr/bin/env bash

cd core
git sparse-checkout set \
'tests/components/smartthings/fixtures' \
'tests/components/smartthings/snapshots'
cd -

git submodule absorbgitdirs core
git submodule update --init --recursive --force core