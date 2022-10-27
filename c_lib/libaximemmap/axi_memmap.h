/******************************************************************************
* Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

int axi_read_words(uint64_t address, unsigned int num_words, unsigned int *buf,
		   int network_order);
int axi_write_words(uint64_t address, unsigned int num_words, unsigned int *buf,
		    int network_order);
