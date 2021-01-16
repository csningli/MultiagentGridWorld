#! /bin/bash

dir="./experiments/"$1
cd $dir

rm *.log

source activate gridworld

config="../../configs/"$2".config"

if [ -f $config ]; then
  python sim.py -c $config
else
  echo "Cannot find the config: "$config
fi
