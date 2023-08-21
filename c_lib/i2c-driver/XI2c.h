/******************************************************************************
* Copyright (C) 2016-2022 Xilinx, Inc.  All rights reserved.
* Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

#ifndef XI2C_H
#define XI2C_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int dev;
    int i2c_fd;
    int IsReady;
} XI2c;

#define XI2C_OPEN_DEVICE_FAILED  3
#define XI2C_COMPONENT_IS_READY 1
#define XI2C_SUCCESS 0
#define XI2C_FAILURE 1

int XI2c_Initialize(XI2c *InstancePtr, int dev);
int XI2c_Release(XI2c *InstancePtr);
int XI2c_ReadINA226Reg(XI2c *InstancePtr, int addr, u_char reg, u_short *val);
int XI2c_WriteINA226Reg(XI2c *InstancePtr, int addr, u_char reg, u_short wr_reg);

#define I2C_SLEEP_US 200 /* I2C sleep period */

#endif
