#!/usr/bin/env bash

./build.sh

docker save surgtoolloc_trial | gzip -c > surgtoolloc_trial.tar.gz
