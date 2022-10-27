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
typedef enum metal_log_level {
	METAL_LOG_EMERGENCY = 0, /**< system is unusable.               */
	METAL_LOG_ALERT, /**< action must be taken immediately. */
	METAL_LOG_CRITICAL, /**< critical conditions.              */
	METAL_LOG_ERROR, /**< error conditions.                 */
	METAL_LOG_WARNING, /**< warning conditions.               */
	METAL_LOG_NOTICE, /**< normal but significant condition. */
	METAL_LOG_INFO, /**< informational messages.           */
	METAL_LOG_DEBUG, /**< debug-level messages.             */
}metal_log_level;
int XHelper_MetalInit(enum metal_log_level loglevel);
void XHelper_MetalSetLogLevel(enum metal_log_level loglevel);
