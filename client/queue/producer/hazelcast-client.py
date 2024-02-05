

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
hqueue = client.get_queue("bounded-queue").blocking()
print("capacity: {}".format(hqueue.remaining_capacity()))
poison_pill = ''
for i in range(100):
    print("offering: {}".format(i))
    hqueue.offer(i)
hqueue.offer(poison_pill)
print("capacity: {}".format(hqueue.remaining_capacity()))
client.shutdown()
