import argparse
import ipfshttpclient
import locale
import random


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="hash value")
args = vars(parser.parse_args() )


import sys
import subprocess

######################
# Test configuration #
######################

ADDR = "/ip4/127.0.0.1/tcp/{0}".format(random.randrange(40000, 65535))



################
# Start daemon #
################
extra_args = {}
if sys.version_info >= (3, 6, 0):
	extra_args["encoding"] = locale.getpreferredencoding()
else:  #PY35: `subprocess.Popen` encoding parameter missing
	extra_args["universal_newlines"] = True

# Spawn IPFS daemon in data directory
print("Starting IPFS daemon on {0}…".format(ADDR), file=sys.stderr)
DAEMON = subprocess.Popen(
	["ipfs", "daemon", "--enable-pubsub-experiment"],
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT,
	**extra_args
)

# Wait for daemon to start up
for line in DAEMON.stdout:
	print("\t{0}".format(line), end="", file=sys.stderr)
	if line.strip() == "Daemon is ready":
		break


client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

print (client.id())

#res = client.cat('QmYezjSSrsVvXLT6nt4eECgRgtLwPmZp6PmsRZcCZRKaTy')
res = client.cat(args["input"])
#print (res)



# Make sure daemon was terminated during the tests
if DAEMON.poll() is None:  # "if DAEMON is running"
   DAEMON.kill()
   print("IPFS daemon was still running after test!", file=sys.stderr)
   output = list(DAEMON.stdout)
   if output:
      print("IPFS daemon printed extra messages:", file=sys.stderr)
      for line in output:
          print("\t{0}".format(line), end="", file=sys.stderr)
