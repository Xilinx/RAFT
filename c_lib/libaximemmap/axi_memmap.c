/******************************************************************************
* Copyright (C) 2021-2022 Xilinx, Inc.  All rights reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "axi_memmap.h"

// axi_open_memory
//
// return handle to /dev/mem device for access

int axi_open_memory()
{
	// Open memory for reading/writing
	//
	// Additional options may help with caching (such as O_DIRECT, O_SYNC), though haven't experimeted
	// Current workaround is to use reserved-memory device type for IQ memory in the device-tree

	int fd;

	fd = open("/dev/mem", O_RDWR);
	if (fd < 1) {
		printf("*** hwc: Error opening memory for reading/writing\n");
	}

	return fd;
}

// axi_close_memory
//
//

void axi_close_memory(int fd)
{
	close(fd);
}

// axi_map_memory
//
// common function to map memory as 32-bit words
// (since this is how MATLAB want to read it)
//
//

int axi_map_memory(uint64_t address, uint64_t page_size, int fd, void **v_ptr,
		   uint64_t *v_offset)
{
	uint64_t p_page_addr;
	uint64_t page_offset;

	void *v_page_ptr;

	// map physical to virtual memory page
	p_page_addr = (address & ~(page_size - 1));
	page_offset = address - p_page_addr;

	v_page_ptr = mmap(NULL, page_size, PROT_READ | PROT_WRITE, MAP_SHARED,
			  fd, p_page_addr);

	if (v_page_ptr == ((void *)-1)) {
		printf("*** hwc: Mapping physical to virtual failed for address=0x%010lX\n",
		       address);
		perror("*** hwc: mmap failed: ");
		exit(-1);
	}

	// update return values
	*v_ptr = v_page_ptr;
	*v_offset = page_offset;

	// success
	return 0;
}

// axi_unmap memory
//
//

int axi_unmap_memory(void *v_ptr, uint64_t page_size)
{
	// flush cache (using msyn)
	//
	// this call currently doesn't compile : different solution is used via setting memory attributes as non-caceable in device tree
	//
	//if (msync(v_page_ptr,page_size,MS_SYNC | MS_INVALIDATE)<0) {
	//  printf("*** hwc: msync at read phy_addr=0x%08X virt_addr=0x%x size=0x%08x\n",address,v_page_ptr,page_size);
	//  perror("*** hwc: msync failed: ");
	//  exit(-1);
	//}

	// unmap memory
	if (munmap(v_ptr, page_size) < 0) {
		perror("*** hwc: munmap failed: ");
		exit(-1);
	}

	// success
	return 0;
}

// axi_read_words
//
// read from num_words from address into tx_buf, applying network byte ordering if network_order!=0

int axi_read_words(uint64_t address, unsigned int num_words, unsigned int *buf,
		   int network_order)
{
	// pointers and variables for virtual to physical mapping
	uint64_t page_size = sysconf(_SC_PAGESIZE);
	uint64_t page_offset;
	void *v_page_ptr;

	unsigned int words;
	unsigned int word_cnt;
	unsigned int k, i;

	unsigned int fd;

	unsigned int idx = 0;

	// open memory
	fd = axi_open_memory();
	//printf("Inside axi_read_words address = %llx num_words = %d Network = %d\n", address, num_words, network_order);

	// AXI Transfer
	word_cnt = num_words;
	while (word_cnt > 0) {
		// map memory
		axi_map_memory(address, page_size, fd, &v_page_ptr,
			       &page_offset);

		// read data words from physical memory
		words = (word_cnt < (page_size - page_offset) / 4) ?
				word_cnt :
				(page_size - page_offset) / 4;
		volatile unsigned *ptr =
			(volatile unsigned *)(v_page_ptr + page_offset);
		for (k = 0; k < words; k++) {
			if (network_order == 0) {
				buf[idx++] = *ptr;
			} else {
				buf[idx++] = htonl(*ptr);
			}
			ptr++;
		}

		// update counts
		word_cnt -= words;
		address += (words * 4);

		// unmap memory
		axi_unmap_memory(v_page_ptr, page_size);
	}

	// close memory
	axi_close_memory(fd);
#if 0
  for(i = 0; i < num_words; i++)
  {
	  printf("axi_read_words buf[%d] = %x\n", i, *(buf+i));
  }
#endif
	// return success
	return 0;
}

// axi_write_words
//
// write num_words to address from buf, reversing network byte ordering if network_order!=0

int axi_write_words(uint64_t address, unsigned int num_words, unsigned int *buf,
		    int network_order)
{
	// pointers and variables for virtual to physical mapping
	uint64_t page_size = sysconf(_SC_PAGESIZE);
	uint64_t page_offset;
	void *v_page_ptr;

	unsigned int words;
	unsigned int word_cnt;
	unsigned int k, i;

	unsigned int fd;

	unsigned int idx = 0;
#if 0
  printf("Inside axi_write_words address = %llx num_words = %d Network = %d\n", address, num_words, network_order);
  for(i = 0; i < num_words; i++)
  {
	  printf("axi_write_words buf[%d] = %x\n", i, *(buf+i));
  }
#endif
	// open memory
	fd = axi_open_memory();

	// AXI Transfer
	word_cnt = num_words;
	while (word_cnt > 0) {
		// map memory
		axi_map_memory(address, page_size, fd, &v_page_ptr,
			       &page_offset);

		// write data words to physical memory
		words = (word_cnt < (page_size - page_offset) / 4) ?
				word_cnt :
				(page_size - page_offset) / 4;
		volatile unsigned *ptr =
			(volatile unsigned *)(v_page_ptr + page_offset);
		for (k = 0; k < words; k++) {
			if (network_order == 0) {
				*ptr = buf[idx++];
			} else {
				*ptr = ntohl(buf[idx++]);
			}
			ptr++;
		}

		// update counts
		word_cnt -= words;
		address += (words * 4);

		// unmap memory
		axi_unmap_memory(v_page_ptr, page_size);
	}

	// close memory
	axi_close_memory(fd);

	// return success
	return 0;
}
