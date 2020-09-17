#!/bin/bash

here=$(dirname ${BASH_SOURCE[0]})

if ! [[ -f $here/.env ]]; then
    cat >"$here/.env" <<EOF
POSTGRES_DB=geomud
POSTGRES_USER=gmuser
POSTGRES_PASS=$(cat /dev/urandom | tr -dc 'A-Za-z0-9_' | fold -w 20 | head -1)
EOF
fi

exec docker-compose "$@"
