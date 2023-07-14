/******************************************************************************
 * Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
 * SPDX-License-Identifier: MIT
 ******************************************************************************/

typedef struct {
  int dev;
  int i2c_fd;
  int IsReady;
} XI2c;

#define XST_OPEN_DEVICE_FAILED 3

int XI2c_Initialize(XI2c *InstancePtr, int dev);
int XI2c_Release(XI2c *InstancePtr);
int XI2c_ReadINA226Reg(XI2c *InstancePtr, int addr, unsigned char reg,
                       unsigned short *val);
int XI2c_WriteINA226Reg(XI2c *InstancePtr, int addr, unsigned char reg,
                        unsigned short wr_reg);

#define I2C_SLEEP_US 200 /* I2C sleep period */
