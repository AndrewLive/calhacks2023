#!/bin/bash

RTSP_URL="rtsp://192.168.42.1:8554/stream0"
OUTPUT_DIR="images"

mkdir -p "$OUTPUT_DIR"

IMAGE_NUM=1
while [ -e "$OUTPUT_DIR/captured_image$IMAGE_NUM.jpg" ]; do
  ((IMAGE_NUM++))
done

ffmpeg -i "$RTSP_URL" -vframes 1 "$OUTPUT_DIR/captured_image$IMAGE_NUM.jpg"

echo "Image captured and saved as captured_image$IMAGE_NUM.jpg"
