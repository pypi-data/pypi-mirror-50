#!/usr/bin/env python
import cli
import sys
from csr_azure_scripts import cas
import argparse
import time

parser = argparse.ArgumentParser(
    description="Capture Packets and upload file to Storage")
parser.add_argument('interface', help='The interface to capture from')
parser.add_argument('container', help='The name of the container to upload to')
parser.add_argument('filename', help='Filename to upload to container')
parser.add_argument('--seconds', help='Seconds to capture', default=10)
args = parser.parse_args()

container = args.container
filename = args.filename

configuration = '''ip access-list extended PKT_CAP
                    permit tcp any any'''
cli.configure(configuration)
cli.execute(
    "monitor capture PKT_CAP access-list PKT_CAP buffer circular size 100")
cmd = "monitor capture PKT_CAP interface %s both" % args.interface
cli.execute(cmd)
cli.execute("monitor capture PKT_CAP clear")
cli.execute("monitor capture PKT_CAP start")

for i in range(0, int(args.seconds)):
    time.sleep(1)
    sys.stdout.write("\r%d secs" % (i+1))
    sys.stdout.flush()

print "\n"

cli.execute("monitor capture PKT_CAP stop")
cmd = "monitor capture PKT_CAP export bootflash:%s" % filename
cli.execute(cmd)

cas().upload_file(container, filename)
