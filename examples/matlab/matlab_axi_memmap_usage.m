%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
% SPDX-License-Identifier: BSD-3-Clause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Put the path of the python module here. It can be in any drive
current_folder = pwd
if count(py.sys.path,current_folder) == 0
    %Put the path of the python module here. It can be in any drive
    insert(py.sys.path,uint32(0),current_folder);
end

%Import the python module in matlab
%rehash toolboxcache
AXI_MEMMAP=py.importlib.import_module('axi_memmap_client');
AXI_MEMMAP=py.importlib.reload(AXI_MEMMAP);

%%%%%% SetIPAndPort
%Input Arguments:
%    arg1: ipaddress of server
%    arg2: port number at server for pyro communication
%Return: None
AXI_MEMMAP.axi_memmap.SetIpAndPort("169.254.10.2", "9090")

%%%%%% axi_write_words
%Input Arguments:
%    arg1: address
%    arg2: number of words
%    arg3: buffer to wirte
%    arg4: network_order
%Return:
%    value1: Success or failure
address = uint32(0xa7c0000)
num_words = uint32(5)
network_order = uint32(0)
buf = py.list({int32(4), int32(5), int32(6), int32(7), int32(8)})
ret = AXI_MEMMAP.axi_memmap.axi_write_words(address, num_words, buf, network_order)

%%%%%% axi_read_words
%    arg1: address
%    arg2: number of words
%    arg3: network_order
%Return:
%    value1: Success or failure
%    value2: read buffer
address = uint32(0xa7c0000)
num_words = uint32(5)
network_order = uint32(0)
ret = AXI_MEMMAP.axi_memmap.axi_read_words(address, num_words, network_order)
S= cell(ret)
retval = ret{1}
readbuf = ret{2}
