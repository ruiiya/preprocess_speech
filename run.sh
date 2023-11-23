#!/bin/bash

stage=1
stop_stage=4

librispeech_url_root='https://www.openslr.org/resources/12'
datasets=('dev-clean' 'dev-other' 'test-clean' 'test-other')

librispeech_path=$PWD/LibriSpeech

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    echo "stage 1: Data Download"
    for index in "${!datasets[@]}"; do
        url="$librispeech_url_root/${datasets[$index]}.tar.gz"
        extract_path="$librispeech_path/${datasets[$index]}"
        if [ ! -f $extract_path ]
        then
            wget -O - $url | tar xz && echo "${datasets[$index]} done" &
            pids[$index]=$!
        fi
    done
    for pid in ${pids[@]}; do
        wait $pid
    done
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    echo "stage 2: Refactor the directories"
    for index in "${!datasets[@]}"; do
        old_path="$librispeech_path/${datasets[$index]}"
        if [[ ${datasets[$index]} =~ "dev" ]]; then
            new_path="$librispeech_path/train/${datasets[$index]}"
        else
            new_path="$librispeech_path/test/${datasets[$index]}"
        fi

        if [ ! -d $new_path ]; then 
            mkdir -p $new_path
        fi

        mv -T $old_path $new_path
    done
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    echo "stage 3: Convert .sph to .wav"
    for f in $(find . -name "*.flac" -type f) ; do 
        sox "$f" "${f%.flac}.wav"
    done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    echo "stage 4: Create Manifest"
    python3 create_manifest.py $librispeech_path

    cat $librispeech_path/test_clean_manifest.json $librispeech_path/test_other_manifest.json > $librispeech_path/test_manifest.json
    cat $librispeech_path/train_clean_manifest.json $librispeech_path/train_other_manifest.json > $librispeech_path/train_manifest.json
fi