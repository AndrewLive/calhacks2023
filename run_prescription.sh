#!/bin/bash

./capture_image.sh

latest_image=$(ls -t images/captured_image*.jpg | head -n 1)

./prescription.py "$latest_image"
