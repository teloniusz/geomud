#!/bin/bash

# patrz: https://gisco-services.ec.europa.eu/distribution/v2/lau/

URL=https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2019_4326.geojson
FNAME=$(basename "$URL")

[[ -f "$FNAME" ]] || wget "$URL"

cat "$FNAME" | jq -cr '.features | map(select(.properties.CNTR_CODE == "PL")) | .[] | "\(.properties.LAU_CODE)@\(.properties.LAU_NAME)@\(.geometry)"' | (
    cat <<EOF
drop table if exists miejsca;
create table miejsca(id serial not null primary key, lau_code varchar(128) not null, name varchar(255) not null, location GEOGRAPHY(Geometry));
create index on miejsca(lau_code);
create index on miejsca(name);
EOF
    IFS=@
    while read -r code name geometry; do
        echo "insert into miejsca (lau_code, name, location) values ('${code}', '${name//\'/\'\'}', ST_GeomFromGeoJSON('${geometry}'));"
    done
)
