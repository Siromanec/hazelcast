import hazelcast
#
# # if __name__ == "__main__":
#
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

hmap = client.get_map("death-map").blocking()

from time import sleep
niter = 1000
total_time = 20
sleep_time = total_time/niter

for k in range(niter):
    sleep(sleep_time)
    if k % 100 == 0:
        print("at: {}".format(k))
    try:
        hmap.put_if_absent(str(k), k)
    except hazelcast.errors.TargetDisconnectedError:
        print("disconnected at: {}".format(k))

print("finished")