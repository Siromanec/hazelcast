import hazelcast
import argparse

poison_pill = ''
#construct the argument parse and parse the arguments
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

while (res := hqueue.take()) != poison_pill:
    print("taken {}".format(res))

hqueue.offer(poison_pill)
print("sent out the poison pill")
client.shutdown()

