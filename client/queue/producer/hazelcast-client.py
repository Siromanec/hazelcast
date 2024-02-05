

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
# from time import sleep
# niter = 1000
# total_time = 20
# sleep_time = total_time/niter
#
# for k in range(niter):
#     sleep(sleep_time)
#     if k % 100 == 0:
#         print("at: {}".format(k))
#     try:
#         hqueue.put_if_absent(str(k), k)
#     except hazelcast.errors.TargetDisconnectedError:
#         print("disconnected at: {}".format(k))
#
# print("finished")