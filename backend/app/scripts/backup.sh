#!/usr/bin/env bash
set -e

# Timestamped filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"

# Environment variables (override with .env)
PGHOST=${PGHOST:-localhost}
PGUSER=${PGUSER:-postgres}
PGPASSWORD=${PGPASSWORD:-postgres}
PGDATABASE=${PGDATABASE:-postgres}

export PGPASSWORD

# Dump database
pg_dump -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -F c -b -v -f "$BACKUP_DIR/db_$TIMESTAMP.dump"

echo "Local backup saved to $BACKUP_DIR/db_$TIMESTAMP.dump"

# Optional S3 upload
if [[ -n "$AWS_BUCKET" ]]; then
  if command -v aws &> /dev/null; then
    aws s3 cp "$BACKUP_DIR/db_$TIMESTAMP.dump" "s3://$AWS_BUCKET/db_$TIMESTAMP.dump"
    echo "Uploaded to s3://$AWS_BUCKET/db_$TIMESTAMP.dump"
  else
    echo "AWS CLI not found; skipping S3 upload"
  fi
fi
