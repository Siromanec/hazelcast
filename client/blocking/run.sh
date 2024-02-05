docker compose stop
docker compose up --build --scale client=3 --scale hazelcast=3 --detach
echo "press Enter to stop"
read
docker compose stop
