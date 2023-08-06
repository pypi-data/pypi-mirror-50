#!/usr/bin/env python
from csr_azure_scripts import cas
import argparse

cmdlist = \
    [
        "show interfaces",
        "show version",
        "show ip route",
        "show platform hardware qfp active statistics drop",
        "show platform hardware qfp active datapath utilization",
        "show interfaces gigabitEthernet 1 | incl drops|pack|err",
        "show platform hardware throughput level",
    ]


parser = argparse.ArgumentParser(description="Upload test file")
parser.add_argument('bucket', help='The name of the bucket to upload to')
parser.add_argument('filename', help='Filename to upload to bucket')
args = parser.parse_args()

csr = cas()
csr.save_cmd_output(cmdlist, args.filename, args.bucket)
