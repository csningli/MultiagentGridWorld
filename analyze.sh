#! /bin/bash

dir="./experiments/"$1

source activate reciprocal

if [ -f $dir"/exp_analyzer.py" ];
then
  cd $dir
  python exp_analyzer.py
else
  log=""
  for file in $dir/*
  do
    if [ ${file: -4} == ".log" ]; then
      log=$file
    fi
  done
  if [ -f $log ]; then
    python analyzer.py -g $log
  else
    echo "Cannot find the log: "$log
  fi
fi
