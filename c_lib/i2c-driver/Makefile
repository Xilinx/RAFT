#
#   {% copyright %}
#

CPU:=aarch64
ROOT_DIR = ../../..
PRJ_ROOT_DIR := app/i2cread

include $(ROOT_DIR)/build/makefile.env
include $(ROOT_DIR)/build/baremetal/makefile.env
include $(ROOT_DIR)/build/makefile.init

APP_NAME = libXI2c.so

XI2c_DIR=.

INCS := \
	-I$(XI2c_DIR) \
	-I$(EMBEDDEDSW_DIR)/lib/bsp/standalone/src/common

# List of the source files
SOURCE_FILES := \
	$(i2read_DIR)/i2cread.c

all: $(APP_NAME)

#utest:

# Library
# Linking

XI2c.o: XI2c.c
	@echo 'Building file: $<'
	$(CC) $(INCS) $(CFLAGS) -MMD -MP -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

# Library
libXI2c.so: XI2c.o
	@echo 'Building target: $@'
	@echo 'Invoking: Library'
#	$(AR) rcs $@.a $(OBJ_PATHS)
	$(CC) XI2c.o --shared -o $@
	@echo 'Finished building target: $@'

cleanit:
	@rm *.o
#include ./baremetal.mk
include $(ROOT_DIR)/build/makefile.rules
#include $(ROOT_DIR)/build/coverity/makefile.rules
#include $(ROOT_DIR)/build/baremetal/makefile.rules
