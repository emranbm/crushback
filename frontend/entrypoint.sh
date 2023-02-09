#!/usr/bin/env sh

set -eu

readonly APP_CONFIG_PATH="/app/frontend/AppConfig.js"
readonly NGINX_CONFIG_PATH="/etc/nginx/conf.d/default.conf"

function main() {
  update_app_config
  update_nginx_config
}

function update_app_config() {
  echo "window.AppConfig = {
      API_BASE_URL: \"$API_BASE_URL\"
  }" > $APP_CONFIG_PATH

  echo "Frontend config updated. Contents of $APP_CONFIG_PATH :"
  cat $APP_CONFIG_PATH
}

function update_nginx_config() {
    envsubst-pattern --prefix NGINX_PARAM_ < "$NGINX_CONFIG_PATH" > "/tmp/nginx.conf"
    mv "/tmp/nginx.conf" "$NGINX_CONFIG_PATH"
    echo "Nginx config updated. Contents of $NGINX_CONFIG_PATH :"
    cat "$NGINX_CONFIG_PATH"
}

main "$@"
