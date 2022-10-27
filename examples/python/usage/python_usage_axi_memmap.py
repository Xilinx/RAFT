# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Anish Kadamathikuttiyil Karthikeyan Pillai"
__copyright__ = "Copyright 2021, Xilinx"

import sys
import datetime
import serpent
import sys
def usage():
    # sys.argv[0] - usage python file name
    # sys.argv[1] - xclient/xcffi/xpyro
    # sys.argv[2] - host/board
    # sys.argv[3] - ip_address
    # sys.argv[4] - port
    print(f"Usage: The application work in three modes xclient, xcffi and xpyro\n"
          f"python3 {sys.argv[0]} xclient host/board ip_address port => Runs at host or board with xclient\n"
          f"sudo python3 {sys.argv[0]} xcffi => Runs at board with xcffi\n"
          f"python3 {sys.argv[0]} xpyro host/board ip_address port => Runs at host or board with xpyro\n"
          f"Example: python3 {sys.argv[0]} xclient host 169.254.10.2 9090")

# 'xcffi' option will run only in the board
if (len(sys.argv) ==  2):
    if (sys.argv[1] != 'xcffi'):
        usage()
        sys.exit()

elif (len(sys.argv) !=  5):
    usage()
    sys.exit()

# The 'xclient' option will run both in host and board
if (sys.argv[1] == 'xclient'):
    # For 'xclient' option the path of the xclient is required
    # The relative path in the host is given for host case
    if (sys.argv[2] == 'host'):
        sys.path.append('../../../xclient/data_stream/data_transfer_no_dma/')
    # The location of xclient in the filesystem is given for the board case
    elif (sys.argv[2] == 'board'):
        sys.path.append('/usr/share/raft/xclient/data_stream/data_transfer_no_dma/')
    else:
        usage()
        sys.exit()
    import axi_memmap_client
    handle = axi_memmap_client.axi_memmap
    ip_address = sys.argv[3]
    port = sys.argv[4]

elif (sys.argv[1] == 'xcffi'):
    # For 'xcffi' option the path of the cffi python code is required
    sys.path.append('/usr/share/raft/xserver/xcffi/drv_api/data_stream/data_transfer_no_dma/')
    from axi_memmap_c import AXI_MEMMAP_C
    handle = AXI_MEMMAP_C()

# The 'xpyro' option will run both in host and board
elif (sys.argv[1] == 'xpyro'):
    ip_address = sys.argv[3]
    port = sys.argv[4]
    import Pyro4
    # Prepare the uri needed for pyro communication
    uri = f"PYRO:AXI_MEMMAP@{ip_address}:{port}"
    handle = Pyro4.Proxy(uri)
else:
    usage()
    sys.exit()

if (sys.argv[1] == 'xclient'):
    #SetIpAndPort
    handle.SetIpAndPort(ip_address, port)

def convert_to_list(data):
    k = []
    for i in range(int(len(data)/4)):
        k.append(int.from_bytes(data[(i*4):(((i+1)*4))], byteorder='little'))
    return k

def convert_to_bytearray(data):
    b = bytearray()
    for i in range(len(data)):
        c = data[i].to_bytes(4, byteorder='little', signed=False)
        b.extend(c)
    return b

def test_axi_write_read():
    buf = [0xABCDEF12, 0x34567890, 0x567890AB, 0x7890ABCD, 0x342ABC12]
    address = 0xa7c0000
    num_words = 5
    network_order = 0
    if (sys.argv[1] == 'xpyro'):
        buf = convert_to_bytearray(buf)
    ret = handle.axi_write_words(address, num_words, buf, network_order)
    assert ret == 0
    ret, buf = handle.axi_read_words(address, num_words, network_order)
    #This conversion is done in xpyro client
    if (sys.argv[1] == 'xpyro'):
        buf = serpent.tobytes(buf)
        buf = convert_to_list(buf)
    assert ret == 0
    assert buf[0] == 0xABCDEF12
    assert buf[1] == 0x34567890
    assert buf[2] == 0x567890AB
    assert buf[3] == 0x7890ABCD
    assert buf[4] == 0x342ABC12

def test_axi_write_read_bulk():
    buf = []
    num_words_write = 1024*2
    num_words = num_words_write
    for i in range (num_words):
        buf.append(0xFFFFFFFF - i)
    address = 0xa7c0000
    network_order = 0
    print("num_words at client test = ", num_words)
    a = datetime.datetime.now()
    if (sys.argv[1] == 'xpyro'):
        buf = convert_to_bytearray(buf)
    ret = handle.axi_write_words(address, num_words, buf, network_order)
    b = datetime.datetime.now()
    c = b-a
    print("Time taken for writing ", num_words * 4, "bytes = ", c.total_seconds(), " seconds")
    print("Write Throughput = ", round((num_words*4)/c.total_seconds()/1000000, 4), "Mega bytes per second")
    assert ret == 0
    num_words = 1024*1000
    a = datetime.datetime.now()
    ret, buf = handle.axi_read_words(address, num_words, network_order)
    #This conversion is done in xpyro client
    if (sys.argv[1] == 'xpyro'):
        buf = serpent.tobytes(buf)
        buf = convert_to_list(buf)
    b = datetime.datetime.now()
    c = b-a
    print("Time taken for reading ", num_words * 4, "bytes = ", c.total_seconds(), " seconds")
    print("Read Throughput = ", round((num_words*4)/c.total_seconds()/1000000,4), "Mega bytes per second")
    for i in range (num_words_write):
        assert buf[i]  == (0xFFFFFFFF - i)

test_axi_write_read()
test_axi_write_read_bulk()
