#!/usr/bin/env bash

HA_VERSION=$1
RAW_URL="https://raw.githubusercontent.com/home-assistant/core/refs/tags/${HA_VERSION}"
TEST_URL="${RAW_URL}/tests/components/smartthings"
MAIN_URL="${RAW_URL}/homeassistant/components/smartthings"

# YQ_VERSION="v4.44.3"
# if ! yq --version 2>/dev/null | grep -q "${YQ_VERSION}"; then
#     echo "Installing yq version ${YQ_VERSION}" >&2
#     wget -qO ~/.local/bin/yq https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64
#     chmod a+x ~/.local/bin/yq
# fi

function update_requirement() {
    requirement=$(echo $1 | cut -d'=' -f1)
    local_file=$(grep "$requirement==" *.txt | cut -d':' -f1)
    remote_file="${RAW_URL}/$(echo ${local_file} | cut -d'.' -f1)"
    local_version=$(grep -E "^$requirement==" $local_file | grep '=='  | cut -d'=' -f3)
    remote_version=$(curl -s "${remote_file}.txt" | grep -E "^$requirement==" | grep '==' | cut -d'=' -f3)

    if [ -z "$remote_version" ]; then
        remote_version=$(curl -s "${remote_file}_all.txt" | grep -E "^$requirement" | grep '==' | cut -d'=' -f3)
    fi
    if [[ $requirement == pysmartthings ]]; then
        echo "Running additional update steps for pysmartthings" >&2
        yq -i ".requirements=[\"homeassistant==${HA_VERSION}\",\"pysmartthings==${remote_version}\"]" custom_components/smartthings/manifest.json
    fi
    
    if [[ $requirement == homeassistant ]]; then
        remote_version=$HA_VERSION
    fi
    # if [[ $requirement == pytest-homeassistant-custom-component ]]; then
    #     remote_version=$(pip list -o | grep pytest-homeassistant-custom-component | awk '{print $3}')
    # fi
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
    elif [[ "$key" == *key:common* ]]; then
        search_key=$(echo $key | sed -r 's/.*key:(common.*)%\].*/\1/g' | sed -r 's/::/./g')
        value=$(jq ".${search_key}" $common_file)
    else
        component=$(echo $key | awk -F':' '{print $4}')
        remote_file="${RAW_URL}/homeassistant/components/${component}/strings.json"
        wget -q $remote_file -O tmp_component_strings.json
        search_key=$(echo $key | sed -r "s/.*key:component::${component}(.*)%\].*/\1/g" | sed -r 's/::/./g')
        value=$(jq "${search_key}" tmp_component_strings.json)
        rm -f tmp_component_strings.json
    fi
    echo $value
}

function update_translations() {
    local_file="custom_components/smartthings/translations/en.json"
    remote_file="${MAIN_URL}/strings.json"
    common_file="${RAW_URL}/homeassistant/strings.json"
    
    wget -q $remote_file -O $local_file
    wget -q $common_file -O tmp_strings.json

    for key in $(yq -r '.. | path | "." + join(".")' $local_file); do
        map_value=$(yq -r "${key} | select(. == \"[%*%]\")" $local_file)
        if [ -z "$map_value" ]; then
            continue
        fi
        value=$(fix_translation $map_value)
        yq -i "${key}=${value}" $local_file
    done

    yq -i '.entity.switch += {"light": {"name": "Display"}, "auto_cleaning_mode": {"name": "Auto Cleaning Mode"}, "spi_mode": {"name": "SPI Mode"}, "volume": {"name": "Sound"}}' $local_file

    rm -f tmp_strings.json
    return
}

echo "Updating requirements for Home Assistant version $HA_VERSION"
echo "-------------------------------------------"
for requirement in $(cat requirements*.txt | grep "=="); do
    update_requirement $requirement
done
# pipenv update

echo "-------------------------------------------"
echo "Updating translations"
echo "-------------------------------------------"
update_translations
echo "-------------------------------------------"