#!/usr/bin/env bash

set -euo pipefail
readonly CWD=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
readonly ROOT_DIR="$CWD/../.."

readonly CRUSHBACK_DB_PASSWORD="$1"
readonly BACKUP_FILE_URL="$2"

if [[ "$BACKUP_FILE_URL" == *\?* ]]; then
  echo "ERROR: URL should not contain query params!"
  echo "Hint: If it's forcefully required, change the script to tolerate '?' in the input URL."
  exit 1
fi

restore_job_manifest=$(helm template "$ROOT_DIR/k8s/helm/crushback-backend" --name-template crushback-backend \
  --set backup.restore.create=true \
  --set backup.restore.backupFileURL="$BACKUP_FILE_URL" \
  --set database.password="$CRUSHBACK_DB_PASSWORD" \
  --show-only templates/restore-job.yaml)

echo "Deleting previous restore job, if exists ..."
echo "$restore_job_manifest" | kubectl delete -f - || true
echo "Creating new restore job ..."
echo "$restore_job_manifest" | kubectl apply -f -
