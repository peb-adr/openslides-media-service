#!/bin/sh

if [ "$APP_CONTEXT" = "dev"   ]; then exec flask --app src/mediaserver run --host 0.0.0.0 --port 9006 --debug; fi
if [ "$APP_CONTEXT" = "tests" ]; then sleep inf; fi
if [ "$APP_CONTEXT" = "prod"  ]; then exec gunicorn -b "0.0.0.0:$MEDIA_PORT" -t "${OPENSLIDES_MEDIA_WORKER_TIMEOUT:-30}" src.mediaserver:app; fi
