#!/bin/bash

#data_name=StateFormer_X64_O0
data_name=Coreutils_X64_O0
data_folder=$HOME/data/bityr/$data_name

decoder=independent
dropout=0
beam_size=4

save_dir=$HOME/results/bityr/$data_name/$decoder-$dropout-$beam_size

if [ ! -e $save_dir ];
then
    mkdir -p $save_dir
fi

export CUDA_VISIBLE_DEVICES=0

python -m src.index \
    train $data_folder/train.pkl $data_folder/validation.pkl \
    -o $save_dir/MODEL.model \
    --optimizer adam \
    --batch_size 32 \
    --glow_decoder_type $decoder \
    --glow_beam_size $beam_size \
    --glow_dropout $dropout \
    --lr 1e-3 \
    --gpu 0 \
    $@
