/******************************************************************************
* Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

/*****************************************************************************/
/**
*
* @file xhelper.c
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
#include <metal/device.h>
#include <metal/log.h>
#include "xhelper.h"

int XHelper_MetalInit(enum metal_log_level loglevel)
{
	struct metal_init_params init_param = METAL_INIT_DEFAULTS;

	init_param.log_level = loglevel;
	/* Initialize libmetal */
	if (0 != metal_init(&init_param)) {
		(void)printf("ERROR: Failed to run metal initialization\n");
		return 1;
	}
	return 0;
}

void XHelper_MetalSetLogLevel(enum metal_log_level loglevel)
{
	metal_set_log_level(loglevel);
	return;
}
