print("i am blocking")
import hazelcast
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cluster-name", required=True, help="name of the cluster")

args = vars(ap.parse_args())
print("Trying to connect to cluster `{}`".format(args["cluster_name"]))

client = hazelcast.HazelcastClient(
    cluster_name=args["cluster_name"],
    cluster_members=["hazelcast"]
)
print("connected to a cluster")
# Create a Distributed Map in the cluster
hmap = client.get_map("counter-map").blocking()

key = "key-normal"
hmap.put_if_absent(key, 0)
for k in range(10_000):
    value = hmap.get(key)
    value += 1
    hmap.put(key, value)

print("finished with {}".format(key))

key = "key-pessimistic"
hmap.put_if_absent(key, 0)
for k in range(10_000):
    hmap.lock(key)
    try:
        value = hmap.get(key)
        value += 1
        hmap.put(key, value)
    finally:
        hmap.unlock(key)
print("finished with {}".format(key))

key = "key-optimistic"
hmap.put_if_absent(key, 0)
for k in range(10_000):
    while True:
        value = hmap.get(key)
        # hqueue.replace_if_same()
        if hmap.replace_if_same(key, value, value + 1):
            break

print("finished with {}".format(key))

