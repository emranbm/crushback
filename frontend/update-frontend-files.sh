#!/usr/bin/env sh

set -eu

readonly FILES_SRC_DIR="/app/"
readonly FILES_DST_DIR="/mnt/frontend/"
readonly APP_CONFIG_PATH="$FILES_DST_DIR/AppConfig.js"

rm -rf $FILES_DST_DIR/*
cp -rf $FILES_SRC_DIR/* $FILES_DST_DIR
echo "window.AppConfig = {
    API_BASE_URL: \"$API_BASE_URL\"
}" > $APP_CONFIG_PATH

echo "Frontend files updated. AppConfig content:"
cat $APP_CONFIG_PATH
