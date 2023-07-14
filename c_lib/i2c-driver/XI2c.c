/*******************************************************************************
 *
 * Copyright (C) 2016 - 2021 Xilinx, Inc.  All rights reserved.
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
/***************************** Include Files *********************************/
#include <stdint.h>
#include <assert.h>
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <stddef.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <errno.h>

#include "XI2c.h"

/************************** Function Implementation *************************/

/****************************************************************************/
/**
*
* I2C linux driver one time initialisation.
*
* @param    InstancePtr is a pointer to the I2c instance.
* @param    dev is the i2c linux device number of the slave device
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note     None
*
****************************************************************************/
int XI2c_Initialize(XI2c *InstancePtr, int dev) {

    char filename[20] = {0};

    assert(InstancePtr != NULL);

    InstancePtr->dev = dev;

    snprintf(filename, 19, "/dev/i2c-%d", dev);

    printf("filename %s\n", filename);
    InstancePtr->i2c_fd = open(filename, O_RDWR);
    if (InstancePtr->i2c_fd < 0) {
        printf("failed to open it %s\n", filename);
        return XI2C_OPEN_DEVICE_FAILED;

    }
    InstancePtr->IsReady = XI2C_COMPONENT_IS_READY;
    return XI2C_SUCCESS;
}

/**
*
* I2C linux driver one time initialisation.
*
* @param    InstancePtr is a pointer to the I2c instance.
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note     None
*
****************************************************************************/
int XI2c_Release(XI2c *InstancePtr) {
    assert(InstancePtr != NULL);
    assert(InstancePtr->IsReady == XI2C_COMPONENT_IS_READY);

    /* unmap mapped memory and close the descriptor */
    close(InstancePtr->i2c_fd);

    return XI2C_SUCCESS;
}

/**
*
* This function is HAL API for I2c read.
*
* @param	File descriptor for the i2c driver.
* @param	Addr address to be read.
* @param	Val read value.
* @param	Len data length.
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note		None
*
****************************************************************************/
int XI2c_ReadData(int File, u_int8_t Addr, u_char *Val, u_char Len)
{
	int ret = XI2C_SUCCESS;
	struct i2c_rdwr_ioctl_data packets;
	struct i2c_msg messages;
	messages.addr = Addr;
	messages.flags = I2C_M_RD;
	messages.len = Len;
	messages.buf = Val;
	packets.msgs = &messages;
	packets.nmsgs = 1;
	if (ioctl(File, I2C_RDWR, &packets) < 0) {
		ret = XI2C_FAILURE;
	}
	usleep(I2C_SLEEP_US);
	return ret;
}

/****************************************************************************/
/**
*
* This function is HAL API for I2c Write Register Address followed by Read
* contents of register
*
* @param	File descriptor for the i2c driver.
* @param	Addr address to be read from.
* @param	reg  register to be read
* @param	val pointer to value to be read to.
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note		None
*
****************************************************************************/
int XI2c_WriteBeforeReadData(int File, u_char Addr, u_char reg, ushort *val)
{
	int ret = XI2C_SUCCESS;
        u_char read_data[2];

        struct i2c_rdwr_ioctl_data packets;
	struct i2c_msg messages[2];
        u_char write_data[1];
        write_data[0] = reg;

	messages[0].addr = Addr;
	messages[0].flags = 0;
	messages[0].len = 1;
	messages[0].buf = write_data;

	messages[1].addr = Addr;
	messages[1].flags = I2C_M_RD;
	messages[1].len = 2;
	messages[1].buf = read_data;


	packets.msgs = (struct i2c_msg *)&messages;
	packets.nmsgs = 2;
	if (ioctl(File, I2C_RDWR, &packets) < 0) {
		ret = XI2C_FAILURE;
	}
	usleep(I2C_SLEEP_US);
        *val = ((read_data[0] << 8)| read_data[1]);
	return ret;
}

/****************************************************************************/
/**
*
* This function is HAL API for I2c write.
*
* @param	File descriptor for the i2c driver.
* @param	Addr address to be written to.
* @param	Val ptr to value to write.
* @param	Len data length.
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note		None
*
****************************************************************************/
int XI2c_WriteData(int File, u_char Addr, u_char *Val, u_char Len)
{
	int ret = XI2C_SUCCESS;
	struct i2c_rdwr_ioctl_data packets;
	struct i2c_msg messages;
	messages.addr = Addr;
	messages.flags = 0;
	messages.len = Len;
	messages.buf = Val;
	packets.msgs = &messages;
	packets.nmsgs = 1;
	if (ioctl(File, I2C_RDWR, &packets) < 0) {
            //LOG;
		ret = XI2C_FAILURE;
	}
	usleep(I2C_SLEEP_US);
	return ret;
}

/****************************************************************************/
/**
*
* This function is top level API for I2C read from INA226 register
*
* @param	InstancePtr ptr to instance of driver
* @param	Addr address of device to be read from.
* @param        reg register number to read from
* @param	val ptr to value to read to
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note		None
*
****************************************************************************/
int XI2c_ReadINA226Reg(XI2c *InstancePtr, int addr, u_char reg, ushort *val)
{
    int ret = 0;
    ret = XI2c_WriteBeforeReadData(InstancePtr->i2c_fd, addr, reg, val);
    if(ret == XI2C_FAILURE)
    {
        printf("Read from INA226 failed\n");
        return(XI2C_FAILURE);
    }
    return(ret);
}

/****************************************************************************/
/**
*
* This function is top level API for I2C read from INA226 register
*
* @param	InstancePtr ptr to instance of driver
* @param	Addr address to be written to.
* @param        reg register number to write to
* @param	val value to write
*
* @return
*	- XI2C_SUCCESS if successful.
*	- XI2C_FAILURE if failed.
*
* @note		None
*
****************************************************************************/

int XI2c_WriteINA226Reg(XI2c *InstancePtr, int addr, u_char reg, ushort val)
{
    int ret = 0;
    	/* Select who to connect to */
    u_char write_data[3];
    write_data[0] = reg;
    write_data[1] = (val >> 8) & 0xff;
    write_data[2] = val & 0xff;
    ret = XI2c_WriteData(InstancePtr->i2c_fd, addr, write_data, 3);
    if(ret == XI2C_FAILURE)
    {
        printf("Write to  INA226 failed\n");
    }
    return(ret);
}
