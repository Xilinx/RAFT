/*******************************************************************************
 *
 * Copyright (C) 2016 - 2020 Xilinx, Inc.  All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
 * OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * Except as contained in this notice, the name of the Xilinx shall not be used
 * in advertising or otherwise to promote the sale, use or other dealings in
 * this Software without prior written authorization from Xilinx.
 *
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
