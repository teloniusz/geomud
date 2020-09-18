#!/bin/bash

here=$(dirname ${BASH_SOURCE[0]})

if ! [[ -f $here/.env ]]; then
    cat >"$here/.env" <<EOF
POSTGRES_DB=geomud
POSTGRES_USER=gmuser
POSTGRES_PASS=$(cat /dev/urandom | tr -dc 'A-Za-z0-9_' | fold -w 20 | head -1)
EOF
fi

tmpdir=
if ! [[ -f $here/camel-router/build/libs/camel-geomud-router-0.0.2.jar ]]; then
    echo "Camel router needs to be built."
    if [[ -z $GRADLE_HOME ]]; then
        echo "Gradle is not found, fetching it to a tempdir."
        tmpdir=$(mktemp -d)
        wget https://services.gradle.org/distributions/gradle-6.6.1-bin.zip -O "$tmpdir/gradle.zip"
        cd "$tmpdir"
        unzip -q gradle.zip
        ln -s gradle-6.6.1 gradle
        cd -
        GRADLE_HOME="$tmpdir/gradle"
    fi
    echo "Building in a docker:"
    docker run -it --rm \
        -v "$GRADLE_HOME:$GRADLE_HOME" -v "$PWD:$PWD" \
        -e "GRADLE_HOME=$GRADLE_HOME" -e "OLD_UID=$(id -u)" -e "OLD_GID=$(id -g)" \
        -w "$PWD/camel-router" \
        openjdk:14 \
        bash -c '$GRADLE_HOME/bin/gradle bootJar; chown -R $OLD_UID:$OLD_GID .'
    [[ -n "$tmpdir" && -d "$tmpdir" && "$tmpdir" = /tmp/* ]] && rm -rf "$tmpdir"
fi

exec docker-compose "$@"
