#!/usr/bin/env bash

HA_VERSION=$1
RAW_URL="https://raw.githubusercontent.com/home-assistant/core/refs/tags/${HA_VERSION}"
TEST_URL="${RAW_URL}/tests/components/smartthings"
MAIN_URL="${RAW_URL}/homeassistant/components/smartthings"

update_requirement() {
    requirement=$1
    local_file=$(grep $requirement *.txt | cut -d':' -f1)
    remote_file="${RAW_URL}/$(echo ${local_file} | cut -d'.' -f1)_all.txt"
    local_version=$(grep -E "^${requirement}==" $local_file | cut -d'=' -f3)
    remote_version=$(curl -s $remote_file | grep -E "^${requirement}==" | cut -d'=' -f3)
    if [ "$local_version" == "$remote_version" ]; then
        echo "No update needed for $requirement"
        return
    fi
    echo "Updating $requirement from $local_version to $remote_version"
    version=$remote_version
    sed -i "s/^${requirement}==.*/${requirement}==${version}/" $local_file
    sed -i "s/^${requirement} = \"==.*\"/${requirement} = \"==${version}\"/" Pipfile
}

fix_translation() {
    key=$1
    local_file="custom_components/smartthings/translations/en.json"
    remote_file="tmp_strings.json"
    if [[ "$key" == *"smartthings"* ]]; then
        search_key=$($key | sed -r 's/.*smartthings(.*)%\]/\1/g' | sed -r 's/::/./g')
        value=$(jq $search_key $local_file)
    else
        search_key=$($key | sed -r 's/.*key:common(.*)%\]/\1/g' | sed -r 's/::/./g')
        value=$(jq $search_key $remote_file)
    fi
}

update_translations() {
    local_file="custom_components/smartthings/translations/en.json"
    remote_file="${RAW_URL}/homeassistant/strings.json"
    wget $remote_file -O tmp_strings.json

    rm -f temp_strings.json
}

for requirement in $(cat requirements*.txt | grep "=="); do
    update_requirement $requirement
done