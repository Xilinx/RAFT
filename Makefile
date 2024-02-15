# Copyright (C) 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: MIT
SUBDIRS := c_lib/i2c-driver c_lib/libaximemmap c_lib/libxhelper c_lib/sysmon-driver

INSTALL_DIR_RAFT := $(DESTDIR)/usr/share/raft
INSTALL_DIR_NOTEBOOKS := ${DESTDIR}/usr/share/notebooks

.PHONY: all clean install $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do \
        	$(MAKE) -C $$dir clean; \
	done

install:
	for dir in $(SUBDIRS); do \
        	$(MAKE) DESTDIR=$(DESTDIR) -C $$dir install; \
	done
	install -d $(INSTALL_DIR_RAFT)
	cp  -r LICENSE docs examples xclient xserver README.md $(INSTALL_DIR_RAFT) 
	echo "Macros: DESTDIR=${DESTDIR}, Notebooks = ${NOTEBOOKS}, \
	STARTUPSC = ${STARTUPSC}, STARTUP = ${STARTUP}, SYSCONF_DIR = ${SYSCONF_DIR}, \
	BINDIR = ${BINDIR}, SYSTEM_UNIT_DIR = ${SYSTEM_UNIT_DIR}  "	

ifeq ($(NOTEBOOKS),enabled)
	echo "Installing Notebooks to ${INSTALL_DIR_NOTEBOOKS}"
	install -d ${INSTALL_DIR_NOTEBOOKS}
	install -m 0755 examples/python/pat/pat20.py ${INSTALL_DIR_NOTEBOOKS}
	install -m 0755 examples/python/pat/Pat20.ipynb ${INSTALL_DIR_NOTEBOOKS}
	install -m 0755 examples/python/rftool/rftool.py ${INSTALL_DIR_NOTEBOOKS}
	install -m 0755 examples/python/rftool/mixer.ipynb ${INSTALL_DIR_NOTEBOOKS}
endif
ifeq ($(STARTUPSC),enabled)
ifneq ($(SYSCONF_DIR),)
	echo "Installing RAFT system controller startup sysconfdir at ${SYSCONF_DIR}"
	install -d ${SYSCONF_DIR}
	install -m 0755 xserver/init/startup/system-controller/raft-startup ${SYSCONF_DIR}
endif
	echo "Installing RAFT  system controller startup to bindir at ${BINDIR}"
	install -d ${BINDIR}
	install -m 0777 xserver/init/startup/system-controller/raft-startup ${BINDIR}
	echo "Installing RAFT system controller startup to system unit dir at${SYSTEM_UNIT_DIR}"
	install -d ${SYSTEM_UNIT_DIR}
	install -m 0644 xserver/init/startup/system-controller/raft-startup.service ${SYSTEM_UNIT_DIR}
endif
ifeq ($(STARTUP), enabled)
ifneq ($(SYSCONF_DIR),)
	echo "Installing RAFT jupyter startup to sysconfdir at ${SYSCONF_DIR}"
	install -d ${SYSCONF_DIR}
	install -m 0755 xserver/init/startup/raftjupyter-startup/raft-startup ${SYSCONF_DIR}
endif
	echo "Installing RAFT jupyter startup to to bindir at ${BINDIR}"
	install -d ${BINDIR}
	install -m 0777 xserver/init/startup/raftjupyter-startup/raft-startup ${BINDIR}
	echo "Installing RAFT jupyter startup to system unit dir at ${SYSTEM_UNIT_DIR}"
	install -d ${SYSTEM_UNIT_DIR}
	install -m 0644 xserver/init/startup/raftjupyter-startup/raft-startup.service ${SYSTEM_UNIT_DIR}
endif


.PHONY: install
