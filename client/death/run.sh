docker compose stop
docker compose up --build --scale client=1 --scale hazelcast=3 --detach
echo "press Enter to test with one dead node"
read -r
docker compose stop
docker compose up --build --scale client=1 --scale hazelcast=3 --detach
sleep 25
docker compose up --scale hazelcast=2 --detach --no-recreate
echo "press Enter to test with two dead nodes"
read -r
docker compose stop
docker compose up --build --scale client=1 --scale hazelcast=3 --detach
sleep 25
docker compose up --scale hazelcast=1 --detach --no-recreate
echo "press Enter to end testing"
read -r
docker compose stop
