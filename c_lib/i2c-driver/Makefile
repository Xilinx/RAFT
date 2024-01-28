# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: MIT
APP = XI2c

LIBSOURCES = *.c
OUTS = *.o
NAME := XI2c
MAJOR = 1
MINOR = 0
VERSION = $(MAJOR).$(MINOR)

all: lib$(NAME).so

lib$(NAME).so.$(VERSION): $(OUTS)
	$(CC) $(LDFLAGS) $(OUTS) -shared -Wl,-soname,lib$(NAME).so.$(MAJOR).$(MINOR) -o lib$(NAME).so.$(VERSION)

lib$(NAME).so: lib$(NAME).so.$(VERSION)
	rm -f lib$(NAME).so.$(MAJOR) lib$(NAME).so
	ln -s lib$(NAME).so.$(VERSION) lib$(NAME).so.$(MAJOR)
	ln -s lib$(NAME).so.$(MAJOR) lib$(NAME).so

%.o: %.c
	$(CC) $(CFLAGS) -c -fPIC $(LIBSOURCES)

clean:
	rm -rf *.o *.so *.so.*
