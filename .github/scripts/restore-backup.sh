#!/usr/bin/env bash

set -euo pipefail
readonly CWD=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
readonly ROOT_DIR="$CWD/../.."

readonly CRUSHBACK_DB_PASSWORD="$1"
readonly DROPBOX_TOKEN="$2"
readonly BACKUP_FILENAME="$3"

restore_job_manifest=$(helm template "$ROOT_DIR/k8s/helm/crushback-backend" --name-template crushback-backend \
  --set backup.restore.create=true \
  --set database.password="$CRUSHBACK_DB_PASSWORD" \
  --set backup.dropboxToken="$DROPBOX_TOKEN" \
  --set backup.restore.backupFilename="$BACKUP_FILENAME" \
  --show-only templates/restore-job.yaml)

echo "Deleting previous restore job, if exists ..."
echo "$restore_job_manifest" | kubectl delete -f - || true
echo "Creating new restore job ..."
echo "$restore_job_manifest" | kubectl apply -f -
