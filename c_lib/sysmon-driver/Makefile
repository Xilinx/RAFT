#
#   {% copyright %}
#

CPU:=aarch64
ROOT_DIR = ../..
PRJ_ROOT_DIR := .

include $(ROOT_DIR)/build/makefile.env
include $(ROOT_DIR)/build/baremetal/makefile.env
include $(ROOT_DIR)/build/makefile.init

APP_NAME = libXSysmon.so sysmon_drv

XSysmon_DIR=.

INCS := \
	-I$(XSysmon_DIR) \
	-I$(EMBEDDEDSW_DIR)/lib/bsp/standalone/src/common

# List of the source files
SOURCE_FILES := \
	$(XSysmon_DIR)/sysmon_drv.c

all: $(APP_NAME)

#utest:

# Library
# Linking

XSysmon.o: XSysmon.c
	@echo 'Building file: $<'
	$(CC) $(INCS) $(CFLAGS) -std=gnu99 -MMD -MP -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

sysmon_drv.o: sysmon_drv.c
	@echo 'Building file: $<'
	$(CC) $(INCS) $(CFLAGS) -std=gnu99 -MMD -MP -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

# Library
libXSysmon.so:: XSysmon.o
	@echo 'Building target: $@'
	@echo 'Invoking: Library'
#	$(AR) rcs $@.a $(OBJ_PATHS)
	$(CC) XSysmon.o --shared -o $@
	@echo 'Finished building target: $@'

sysmon_drv: sysmon_drv.o XSysmon.o

cleanit:
	@rm *.o *.so
#include ./baremetal.mk
#include $(ROOT_DIR)/build/makefile.rules
#include $(ROOT_DIR)/build/coverity/makefile.rules
#include $(ROOT_DIR)/build/baremetal/makefile.rules
