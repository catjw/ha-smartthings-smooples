#!/usr/bin/env bash

HA_VERSION=$1
RAW_URL="https://raw.githubusercontent.com/home-assistant/core/refs/tags/${HA_VERSION}"
TEST_URL="${RAW_URL}/tests/components/smartthings"
MAIN_URL="${RAW_URL}/homeassistant/components/smartthings"

function update_requirement() {
    requirement=$1
    local_file=$(grep $requirement *.txt | cut -d':' -f1)
    common__file="${RAW_URL}/$(echo ${local_file} | cut -d'.' -f1)_all.txt"
    local_version=$(grep -E "^${requirement}==" $local_file | cut -d'=' -f3)
    remote_version=$(curl -s $common__file | grep -E "^${requirement}==" | cut -d'=' -f3)
    if [ "$local_version" == "$remote_version" ]; then
        echo "No update needed for $requirement"
        return
    fi
    echo "Updating $requirement from $local_version to $remote_version" >&2
    version=$remote_version
    sed -i "s/^${requirement}==.*/${requirement}==${version}/" $local_file
    sed -i "s/^${requirement} = \"==.*\"/${requirement} = \"==${version}\"/" Pipfile
}

function fix_translation() {
    key=$1
    echo "Fixing translation for ${key}" >&2
    local_file="custom_components/smartthings/translations/en.json"
    common_file="tmp_strings.json"
    if [[ "$key" == *smartthings* ]]; then
        search_key=$(echo $key | sed -r 's/.*smartthings(.*)%\].*/\1/g' | sed -r 's/::/./g')
        value=$(jq "${search_key}" $local_file)
    else
        search_key=$(echo $key | sed -r 's/.*key:(common.*)%\].*/\1/g' | sed -r 's/::/./g')
        value=$(jq ".${search_key}" $common_file)
    fi
    echo $value
}

function update_translations() {
    local_file="custom_components/smartthings/translations/en.json"
    remote_file="${MAIN_URL}/strings.json"
    common_file="${RAW_URL}/homeassistant/strings.json"
    
    wget $remote_file -O $local_file

    wget $common_file -O tmp_strings.json

    grep -n "\[%" $local_file | (while read line_number line; do
        line_number=$(echo $line_number | cut -d':' -f1)
        value=$(fix_translation $(echo $line | cut -d' ' -f2))
        sed -ir "${line_number}s/\"\[%.*%\]\"/${value}/" $local_file
    done)

    echo "Adding new translations" >&2
    cp $local_file temp_strings.json
    jq '.entity.switch += {light: {name: "Display"}, auto_cleaning_mode: {name: "Auto Cleaning Mode"}, spi_mode: {name: "SPI Mode"}, volume: {name: "Sound"}}' tmp_strings.json > $local_file

    rm -rf tmp_strings.json
    return
}

echo "Updating requirements for Home Assistant version $HA_VERSION"
echo "-------------------------------------------"
for requirement in $(cat requirements*.txt | grep "=="); do
    update_requirement $requirement
done

echo "-------------------------------------------"
echo "Updating translations"
echo "-------------------------------------------"
update_translations
echo "-------------------------------------------"