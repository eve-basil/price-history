#!/bin/sh

##
# Ensure these are all set in the environment
#
# export DB_HOST=
# export DB_NAME=
# export DB_USER=
# export DB_PASS=
export WEB_WORKERS=${WEB_WORKERS:-'2'}
export WEB_PORT=${WEB_PORT:-'8081'}
export WEB_HOST=${WEB_HOST:-'0.0.0.0'}
export APP_ENV=${APP_ENV:-'production'}
export WEB_OPTS=${WEB_OPTS:-''}

OPTS="--access-logfile - --error-logfile - -b ${WEB_HOST}:${WEB_PORT} \
    ${WEB_OPTS}"

if [ "${APP_ENV}" = "production" ]; then
    OPTS="${OPTS} -k gevent --preload"
else
    OPTS="${OPTS} --reload --log-level debug"
fi

if [ ! -d log ];then
  mkdir log
fi
gunicorn ${OPTS} basil.prices.server >> logs/prices.log 2>&1
