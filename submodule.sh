#! /usr/bin/env bash


git submodule init core
git clone --no-checkout --depth=1 $(git config submodule.core.url) core

cd core
git sparse-checkout set \
'tests/components/smartthings/fixtures' \
'tests/components/smartthings/snapshots'
cd -

git submodule absorbgitdirs core
git submodule update --init --recursive --force core