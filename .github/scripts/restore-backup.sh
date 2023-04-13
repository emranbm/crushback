#!/usr/bin/env bash

set -euo pipefail
readonly CWD=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
readonly ROOT_DIR="$CWD/../.."

readonly CRUSHBACK_DB_PASSWORD="$1"
readonly S3_ACCESS_KEY_ID="$2"
readonly S3_SECRET_KEY="$3"
readonly BACKUP_FILENAME="$4"

restore_job_manifest=$(helm template "$ROOT_DIR/k8s/helm/crushback-backend" --name-template crushback-backend \
  --set backup.restore.create=true \
  --set database.password="$CRUSHBACK_DB_PASSWORD" \
  --set backup.s3.accessKey="$S3_ACCESS_KEY_ID" \
  --set backup.s3.secretKey="$S3_SECRET_KEY" \
  --set backup.restore.backupFilename="$BACKUP_FILENAME" \
  --show-only templates/restore-job.yaml)

echo "Deleting previous restore job, if exists ..."
echo "$restore_job_manifest" | kubectl delete -f - || true
echo "Creating new restore job ..."
echo "$restore_job_manifest" | kubectl apply -f -
