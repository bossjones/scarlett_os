#!/usr/bin/env bash

if [[ "${1}" != "" ]]
then
  iconv -f utf-8 -t utf-8 -c $1
else
  echo -e "[Error] please set a file you want to run this on\n"
