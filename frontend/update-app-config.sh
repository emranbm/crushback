#!/usr/bin/env sh

set -eu

readonly APP_CONFIG_PATH="/app/frontend/AppConfig.js"

echo "window.AppConfig = {
    API_BASE_URL: \"$API_BASE_URL\"
}" > $APP_CONFIG_PATH

echo "Frontend files updated. AppConfig content:"
cat $APP_CONFIG_PATH
