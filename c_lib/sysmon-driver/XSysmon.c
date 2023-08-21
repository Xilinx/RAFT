/******************************************************************************
* Copyright (C) 2016-2022 Xilinx, Inc.  All rights reserved.
* Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/
#define _GNU_SOURCE
#include "XSysmon.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <dirent.h>
#include <errno.h>
#include <ctype.h>

const char *iio_dir = "/sys/bus/iio/devices/";

/**
 * read_sysfs_posint() - read an integer value from file
 * @filename: name of file to read from
 * @basedir: the sysfs directory in which the file is to be found
 *
 * Returns the read integer value >= 0 on success, otherwise a negative error
 * code.
 **/
int read_sysfs_posint(const char *filename, const char *basedir)
{
	int ret;
	FILE *sysfsfp;
	char *temp = malloc(strlen(basedir) + strlen(filename) + 2);

	if (!temp) {
		fprintf(stderr, "Memory allocation failed");
		return -ENOMEM;
	}

	ret = sprintf(temp, "%s/%s", basedir, filename);
	if (ret < 0)
		goto error_free;

	sysfsfp = fopen(temp, "r");
	if (!sysfsfp) {
		ret = -errno;
		goto error_free;
	}

	errno = 0;
	if (fscanf(sysfsfp, "%d\n", &ret) != 1) {
		ret = errno ? -errno : -ENODATA;
		if (fclose(sysfsfp))
			perror("read_sysfs_posint(): Failed to close dir");

		goto error_free;
	}

	if (fclose(sysfsfp))
		ret = -errno;

error_free:
	free(temp);

	return ret;
}

/**
 * read_sysfs_int() - read an integer value from file
 * @filename: name of file to read from
 * @basedir: the sysfs directory in which the file is to be found
 *
 * Returns ret <=0 on failure otherwise value in val
 * code.
 **/
int read_sysfs_int(const char *filename, const char *basedir, int *val)
{
	int ret;
	FILE *sysfsfp;
	char *temp = malloc(strlen(basedir) + strlen(filename) + 2);

	if (!temp) {
		fprintf(stderr, "Memory allocation failed");
		return -ENOMEM;
	}

	ret = sprintf(temp, "%s/%s", basedir, filename);
	if (ret < 0)
		goto error_free;

	sysfsfp = fopen(temp, "r");
	if (!sysfsfp) {
		ret = -errno;
		goto error_free;
	}

	errno = 0;
	if (fscanf(sysfsfp, "%d\n", val) != 1) {
		ret = errno ? -errno : -ENODATA;
		if (fclose(sysfsfp))
			perror("read_sysfs_posint(): Failed to close dir");

		goto error_free;
	}

	if (fclose(sysfsfp))
		ret = -errno;

error_free:
	free(temp);

	return ret;
}

/**
 * read_sysfs_float() - read a float value from file
 * @filename: name of file to read from
 * @basedir: the sysfs directory in which the file is to be found
 * @val: output the read float value
 *
 * Returns a value >= 0 on success, otherwise a negative error code.
 **/
int read_sysfs_float(const char *filename, const char *basedir, float *val)
{
	int ret = 0;
	FILE *sysfsfp;
	char *temp = malloc(strlen(basedir) + strlen(filename) + 2);

	if (!temp) {
		fprintf(stderr, "Memory allocation failed");
		return -ENOMEM;
	}

	ret = sprintf(temp, "%s/%s", basedir, filename);
	if (ret < 0)
		goto error_free;

	sysfsfp = fopen(temp, "r");
	if (!sysfsfp) {
		ret = -errno;
		goto error_free;
	}

	errno = 0;
	if (fscanf(sysfsfp, "%f\n", val) != 1) {
		ret = errno ? -errno : -ENODATA;
		if (fclose(sysfsfp))
			perror("read_sysfs_float(): Failed to close dir");

		goto error_free;
	}

	if (fclose(sysfsfp))
		ret = -errno;

error_free:
	free(temp);

	return ret;
}

/**
 * read_sysfs_string() - read a string from file
 * @filename: name of file to read from
 * @basedir: the sysfs directory in which the file is to be found
 * @str: output the read string
 *
 * Returns a value >= 0 on success, otherwise a negative error code.
 **/
int read_sysfs_string(const char *filename, const char *basedir, char *str)
{
	int ret = 0;
	FILE *sysfsfp;
	char *temp = malloc(strlen(basedir) + strlen(filename) + 2);

	if (!temp) {
		fprintf(stderr, "Memory allocation failed");
		return -ENOMEM;
	}

	ret = sprintf(temp, "%s/%s", basedir, filename);
	if (ret < 0)
		goto error_free;

	sysfsfp = fopen(temp, "r");
	if (!sysfsfp) {
		ret = -errno;
		goto error_free;
	}

	errno = 0;
	if (fscanf(sysfsfp, "%s\n", str) != 1) {
		ret = errno ? -errno : -ENODATA;
		if (fclose(sysfsfp))
			perror("read_sysfs_string(): Failed to close dir");

		goto error_free;
	}

	if (fclose(sysfsfp))
		ret = -errno;

error_free:
	free(temp);

	return ret;
}

/**
 * XSysmon_ReadValue() - read a float value from Sysmon
 * @strId: Sysmon field name root as it appears in sys fs
 * @value: float value to output
 *
 * Returns a value >= 0 on success, otherwise a negative error code.
 **/

int XSysmon_ReadValue(char *strId, float *value)
{
	int raw, offset;
	char file[60] = {};
	int ret = 0;

	file[0] = 0;
	strcat(file, strId);
	strcat(file, "_raw");

	raw = read_sysfs_posint(file, "/sys/bus/iio/devices/iio:device0/");
	if (ret < 0) {
		return (XSYSMON_FAILURE);
	}
	file[0] = 0;
	strcat(file, strId);
	strcat(file, "_scale");

	float scale;
	ret = read_sysfs_float(file, "/sys/bus/iio/devices/iio:device0/",
			       &scale);

	if (ret < 0) {
		return (XSYSMON_FAILURE);
	}

	if (strstr(file, "temp") == NULL) {
		*value = raw * scale / 1000;
	} else {
		file[0] = 0;
		strcat(file, strId);
		strcat(file, "_offset");
		ret = read_sysfs_int(file, "/sys/bus/iio/devices/iio:device0/",
				     &offset);
		if (ret < 0) {
			return (XSYSMON_FAILURE);
		}
		*value = (raw + offset) * scale / 1000;
	}
	return (XSYSMON_SUCCESS);
}
