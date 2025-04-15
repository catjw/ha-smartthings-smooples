#! /usr/bin/env bash


git submodule update --init --recursive --force core

cd core
git sparse-checkout set \
'tests/components/smartthings/fixtures' \
'tests/components/smartthings/snapshots'

git checkout tags/$(grep homeassistant== ../requirements.test.txt  | awk -F"=" '{print $3}')
cd -

git submodule absorbgitdirs core
git submodule update --init --recursive --force core