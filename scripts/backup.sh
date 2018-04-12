#!/bin/sh
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
mkdir -p backups
timestamp=$(date +'%Y-%m-%d-%H-%M-%S')
cp -r data/results backups/$timestamp
