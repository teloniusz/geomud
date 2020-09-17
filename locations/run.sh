here=$(dirname ${BASH_SOURCE[0]})
docker run -v "$here:/app" --env-file "$here/../.env" -it tiangolo/uwsgi-nginx-flask:python3.8
