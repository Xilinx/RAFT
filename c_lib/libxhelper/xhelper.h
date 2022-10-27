/******************************************************************************
* Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

/*****************************************************************************/
/**
*
* @file xhelper.h
* @addtogroup xhelper_v1_0
* @{
*
* Contains the APIs for DFE Mixer component.
*
* <pre>
* MODIFICATION HISTORY:
*
* Ver   Who    Date     Changes
* ----- ---    -------- -----------------------------------------------
* 1.0   akk    03/29/21 Initial version
* </pre>
*
******************************************************************************/

#include <metal/log.h>
int XHelper_MetalInit(enum metal_log_level loglevel);
void XHelper_MetalSetLogLevel(enum metal_log_level loglevel);
