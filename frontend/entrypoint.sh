#!/usr/bin/env sh

set -eu

readonly APP_CONFIG_PATH="/app/frontend/AppConfig.js"

function main() {
  update_app_config
}

function update_app_config() {
  echo "window.AppConfig = {
      API_BASE_URL: \"$API_BASE_URL\"
  }" > $APP_CONFIG_PATH

  echo "Frontend config updated. Contents of $APP_CONFIG_PATH :"
  cat $APP_CONFIG_PATH
}

main "$@"
