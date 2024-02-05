docker compose stop
docker compose up --build --detach --scale consumer=4 --scale producer=1