/******************************************************************************
* Copyright (C) 2017 - 2021 Xilinx, Inc.  All rights reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

/*****************************************************************************/
/**
*
* @file xrfclk.h
* @addtogroup xrfclk
* @{
*
* Contains the API of the XRFclk middleware.
*
* <pre>
* MODIFICATION HISTORY:
*
* Ver   Who    Date     Changes
* ----- ---    -------- -----------------------------------------------
* 1.0   dc     07/21/19 Initial version
* 1.1   dc     11/21/19 Remove xil dependencies from linux build
*       dc     11/25/19 update LMX and LMK configs
*       dc     12/05/19 adjust LMX and LMK configs to a rftool needs
* 1.2   dc     22/01/20 add version and list of LMK frequencies
*       dc     03/05/20 add protection for shared i2c1 MUX
* 1.3   dc     03/10/20 update LMK/LMX config for MTS
* 1.4   dc     03/30/20 new LMX config suppressing RF noise on dual output
* </pre>
*
******************************************************************************/

typedef unsigned char u8;
typedef unsigned int u32;
typedef int s32;
#define XST_SUCCESS 0L
#define XST_FAILURE 1L

#define RFCLK_LMX2594_1 0 /* I0 on MUX and SS3 on Bridge */
#define RFCLK_LMX2594_2 1 /* I1 on MUX and SS2 on Bridge */
#define RFCLK_LMK 2 /* I2 on MUX and SS1 on Bridge */
#define RFCLK_CHIP_NUM 3
#define LMK_COUNT 128
#define LMK_FREQ_NUM 2 /* Number of LMK freq. configs */
#define LMX_ADC_NUM 8 /* Number of LMX ADC configs */
#define LMX_DAC_NUM 24 /* Number of LMX DAC configs */

#define LMX2594_COUNT 116
#define FREQ_LIST_STR_SIZE 50 /* Frequency string size */

u32 XRFClk_WriteReg(u32 ChipId, u32 Data);
u32 XRFClk_ReadReg(u32 ChipId, u32 *Data);
u32 XRFClk_Init(int GpioId);
void XRFClk_Close();
u32 XRFClk_ResetChip(u32 ChipId);
u32 XRFClk_SetConfigOnOneChipFromConfigId(u32 ChipId, u32 ConfigId);
u32 XRFClk_SetConfigOnOneChip(u32 ChipId, u32 *cfgData, u32 len);
u32 XRFClk_GetConfigFromOneChip(u32 ChipId, u32 *cfgData);
u32 XRFClk_SetConfigOnAllChipsFromConfigId(u32 ConfigId_LMK, u32 ConfigId_RF1,
					   u32 ConfigId_RF2);
u32 XRFClk_ControlOutputPortLMK(u32 PortId, u32 state);
u32 XRFClk_ConfigOutputDividerAndMUXOnLMK(u32 PortId, u32 DCLKoutX_DIV,
					  u32 DCLKoutX_MUX, u32 SDCLKoutY_MUX,
					  u32 SYSREF_DIV);

/** @} */
