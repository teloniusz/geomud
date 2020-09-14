#!/bin/sh

docker run -it --rm -v pipcache:/root/.cache/pip -v $PWD:$PWD -e PYTHONPATH=$PWD -w $PWD python:3.8 bash -c 'exec ./mud.py'
