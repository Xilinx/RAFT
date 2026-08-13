# Copyright (C) 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
# SPDX-License-Identifier: MIT
SUBDIRS := c_lib/i2c-driver c_lib/libaximemmap c_lib/libxhelper c_lib/sysmon-driver

INSTALL_DIR_RAFT := $(DESTDIR)/usr/share/raft
INSTALL_DIR_NOTEBOOKS := ${DESTDIR}/usr/share/notebooks
PM_CMD_PY := ${DESTDIR}/usr/share/raft/examples/python/pmtool/pm-cmd.py
LINK_NAME := $(BINDIR)/raft-pm-cmd

.PHONY: all clean install $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do \
        	$(MAKE) -C $$dir clean; \
	done
	rm -f $(LINK_NAME)

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
	echo "Installing symbolic link for pm-cmd CLI App: $(LINK_NAME) -> $(PM_CMD_PY)"
	install -d ${BINDIR}
	ln --relative --symbolic -f $(PM_CMD_PY) $(LINK_NAME)
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
	install -m 0644 examples/python/pmcapture/pmcapture.service ${SYSTEM_UNIT_DIR}
	install -d ${INSTALL_DIR_RAFT}/examples/python/pmcapture
	install -m 0755 examples/python/pmcapture/pmcapture ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/board_config.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/capture_config.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/capture_daemon.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/capture_output.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/capture_session.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/sampler_engine.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/gpio_resolve.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0755 examples/python/pmcapture/trigger_monitor.py ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0644 examples/python/pmcapture/pmcapture.service ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -m 0644 examples/python/pmcapture/pmcapture.1 ${INSTALL_DIR_RAFT}/examples/python/pmcapture/
	install -d ${DESTDIR}/usr/share/man/man1
	install -m 0644 examples/python/pmcapture/pmcapture.1 ${DESTDIR}/usr/share/man/man1/
	ln --relative --symbolic -f ${INSTALL_DIR_RAFT}/examples/python/pmcapture/pmcapture $(BINDIR)/pmcapture
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
