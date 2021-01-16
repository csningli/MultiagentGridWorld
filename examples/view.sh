#! /bin/bash

source activate reciprocal

config="./configs/"$1".config"

if [ -f $config ]; then
  python viewer.py -c $config -w 300 -t 300
else
  echo "Cannot find the config: "$config
fi
