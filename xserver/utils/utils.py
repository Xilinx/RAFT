# Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

__author__ = "Dragan Cvetic"
__copyright__ = "Copyright 2021, Xilinx"

import logging
import base64
from cffi import FFI
import os
import sys

RAFT_DIR = '/usr/share/raft/'
DEFAULT_PORT_NUMBER=9090

ffi = FFI()


def open_c_library(c_libhdr, c_lib):
    file_data = None
    lib_handle = None
    hdr = None
    try:
        hdr = open(c_libhdr, "r")
        file_data = hdr.read()
        ffi.cdef(file_data)
        hdr.close()
    except FileNotFoundError:
        logging.error("[xserver]: Unable to find '%s'" % c_libhdr)
        pass
    except IOError:
        logging.error("[xserver]: Unable to open '%s'" % c_libhdr)
        pass
    try:
        lib_handle = ffi.dlopen(c_lib)
    except IOError:
        logging.error("[xserver]: Unable to open '%s'" % c_lib)
        pass
    return lib_handle

def open_packed_c_library(c_libhdr, c_lib):
    file_data = None
    lib_handle = None
    hdr = None
    try:
        hdr = open(c_libhdr, "r")
        file_data = hdr.read()
        ffi.cdef(file_data, pack=1)
        hdr.close()
    except FileNotFoundError:
        logging.error("[xserver]: Unable to find '%s'" % c_libhdr)
        pass
    except IOError:
        logging.error("[xserver]: Unable to open '%s'" % c_libhdr)
        pass
    try:
        lib_handle = ffi.dlopen(c_lib)
    except IOError:
        logging.error("[xserver]: Unable to open '%s'" % c_lib)
        pass
    return lib_handle


def struct_to_py(CdataPtr, TypeFields):
    for Fld, FldType in TypeFields:
        if FldType.type.kind == 'primitive':
            yield (Fld, getattr(CdataPtr, Fld))
        else:
            yield (Fld, cdata_to_py(getattr(CdataPtr, Fld)))


def array_to_py(CdataPtr):
    Type = ffi.typeof(CdataPtr)
    if Type.item.kind == 'primitive':
        if Type.item.cname == 'wchar_t' or Type.item.cname == 'char':
            return ffi.string(CdataPtr)
        else:
            return [CdataPtr[m] for m in range(Type.length)]
    else:
        return [cdata_to_py(CdataPtr[m]) for m in range(Type.length)]


def cdata_to_py(CdataPtr):
    Type = ffi.typeof(CdataPtr)
    if Type.kind == 'struct':
        return dict(struct_to_py(CdataPtr, Type.fields))
    elif Type.kind == 'primitive':
        return int(CdataPtr)
    elif Type.kind == 'array':
        return array_to_py(CdataPtr)

def cptr_to_pylist(CdataPtr, len):
    List = []
    for i in range(len):
        List.append(CdataPtr[i])
    return List

def cdata_string_to_py(CdataPtr):
    return ffi.string(CdataPtr)

def extract_b64_encoded_string(var):
    # if it is b64 encoded, extract the data
    if isinstance(var, dict):
        b64_data = var['data']
        b64_bytes_data = b64_data.encode('ascii')
        msg_bytes_data = base64.b64decode(b64_bytes_data)
        data = msg_bytes_data.decode('ascii')
    # otherwise, consider it as a string and return it
    else:
        data = var
    data = bytes(data, 'utf-8')
    return data

def get_ip_and_port():
    if (len(sys.argv) > 1):
        ipaddr = sys.argv[1]
    else:
        handle = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'')
        ipaddr = handle.read().strip()
        handle.close()

    if (len(sys.argv) > 2):
        port = int(sys.argv[2])
    else:
        port = DEFAULT_PORT_NUMBER

    return ipaddr, port

def convert_to_bytearray(data):
    bb = bytearray()
    for i in range(len(data)):
        c = data[i].to_bytes(4, byteorder='little', signed=False)
        bb.extend(c)
    return bb

def convert_to_list(data):
    k = []
    for i in range(int(len(data)/4)):
        k.append(int.from_bytes(data[(i*4):(((i+1)*4))], byteorder='little'))
    return k

def get_python_log_levels():
    python_log_level = {
        "DEBUG": 4,
        "INFO": 3,
        "WARNING": 2,
        "ERROR": 1,
        "CRITICAL": 0
    }
    return python_log_level

def getkey_from_listbeginvalue(dictionary, value):
    found = 0
    key = 0
    for key, listvalue in dictionary.items():
        if listvalue[0] == value:
            found = 1 
            break
    return found, key 

xhelper_handle = open_c_library(RAFT_DIR + "xserver/xcffi/drv_header/board_common/xhelper.h", "/usr/lib/libxhelper.so.1")
