# Copyright (C) 2026 Advanced Micro Devices, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

# Client side of the pmcapture I2C bus arbitration protocol.
#
# The System Controller has three independent I2C accessors: the pmcapture
# daemon, sc_appd, and this xserver PM service.  pmcapture owns
# /run/pmcapture/control.sock and acts as the arbiter; the other two ask it
# for an exclusive window before touching the bus and hand the window back
# when they are done.
#
# Arbitration is cooperative rather than enforced by the kernel, so the rule
# is to fail closed: the bus is touched only when an acquire was granted.
#
#   * An absent socket is the one exception, and it is silent.  No pmcapture
#     is running, so the bus is used as it was before arbitration.
#
#   * Once a socket exists the arbiter is expected to answer.  A stale socket
#     refusing connect(), a daemon that accepts and never replies, a closed
#     connection or an unreadable reply all raise BusUnavailable, because
#     from this end a daemon that is mid-capture cannot be told apart from
#     one that has gone away.
#
#   * A refusal is a real conflict (a capture is running, or another holder
#     owns the window).  It is reported to the caller instead of being
#     swallowed, so the operation fails loudly rather than returning
#     readings corrupted by an interleaved transfer.

__author__ = "Advanced Micro Devices, Inc."
__copyright__ = "Copyright 2026, Advanced Micro Devices, Inc."

import contextlib
import json
import logging
import os
import socket
import threading

PMCAPTURE_SOCK = "/run/pmcapture/control.sock"
# An idle handshake over a local Unix socket is sub-millisecond, so a second
# is three orders of magnitude of headroom for a loaded SC.  It is also the
# whole delay a caller can see when the daemon is wedged, since no release is
# sent when the acquire did not grant.
PMCAPTURE_TIMEOUT = 1  # seconds
HOLDER = "raft-xserver-pm"

# Fixed string carried in the "error" member of the PM failure envelope
# whenever the bus was not granted, whatever the cause.  Clients test for it
# rather than reading the message text: raft-pm-cmd uses it to print the same
# fixed wording as the other arbitrating clients, and BEAM can recognize the
# condition without matching prose.  The "message" member still carries the specific reason for
# anything that wants to show it.
I2C_DENIED = "i2c_arbitration_denied"


# pmcapture refused the bus because another participant is using it.
class BusBusy(Exception):
    pass


# A socket exists but the arbiter gave no usable answer, so the bus must not
# be touched.  Derived from BusBusy so that every caller already handling a
# refusal — above all PM.handle_request(), which turns it into RAFT's normal
# failure envelope — treats an unreachable arbiter the same way, while the
# message still says which of the two happened.
class BusUnavailable(BusBusy):
    pass


# Reentrant handle on the pmcapture exclusive window.
#
# A single xserver process serves every RAFT client, and Pyro may run
# handlers on more than one thread, so the depth counter and the socket
# exchange are both guarded.  Nesting matters because a coarse operation
# such as GetValuesAll() reads many rails under one window; only the
# outermost acquire talks to the daemon.
class BusLock(object):

    # Set up the socket path, holder identity, and depth bookkeeping.
    def __init__(self, sock_path=PMCAPTURE_SOCK, holder=HOLDER):
        self._sock_path = sock_path
        self._holder = holder
        self._mutex = threading.RLock()

        # How many acquire() calls are currently outstanding, so that nested
        # windows cost one handshake rather than one per level.  0 means no
        # window is open.  The first acquire() sets it to 1 and is the only
        # one that asks the daemon; an acquire() that finds it non-zero just
        # increments and returns.  release() decrements, and only the call
        # that brings it back to 0 sends "release".  The count belongs to the
        # process rather than a thread, so concurrent Pyro handlers share one
        # window that stays open until the last of them releases.  A release()
        # with no matching acquire() finds 0 and returns untouched.
        self._depth = 0

        # Whether the daemon actually granted the window.  An acquire() that
        # found no socket still counts depth, but leaves this False so no
        # "release" is sent for a window that was never granted.
        self._granted = False

        self._logger = logging.getLogger(__name__)

    # The socket is there but yielded no usable reply, so refuse the bus.
    # Never returns; callers can write "return self._unavailable(...)" to
    # make that obvious at the call site.
    #
    # The message names the socket and the cause, since this is what reaches
    # the caller as its failure message and what PM.handle_request() logs.
    def _unavailable(self, cmd, reason):
        raise BusUnavailable(
            f"pmcapture {cmd} failed on {self._sock_path}: {reason}"
        )

    # Run one request/response round trip against the control socket.
    # Returns the decoded reply, or None when there is no socket at all,
    # which the callers treat as "no pmcapture on this board".  Raises
    # BusUnavailable when a socket is present but answers nothing usable.
    def _exchange(self, cmd):
        request = {"cmd": cmd, "holder": self._holder, "pid": os.getpid()}

        # Deliberately silent: no socket means the board does not run
        # pmcapture, so there is nothing to arbitrate and nothing worth
        # reporting.  sc_appd's access() check returns the same way.
        if not os.path.exists(self._sock_path):
            return None

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(PMCAPTURE_TIMEOUT)
                sock.connect(self._sock_path)
                sock.sendall((json.dumps(request) + "\n").encode())

                # recv() returns at most 4096 bytes per call and a stream
                # socket may split the reply, so read until the newline
                # that terminates it rather than assuming one call is
                # enough.  An empty chunk means the daemon closed the
                # connection without ever sending that newline.
                buffer = b""
                while b"\n" not in buffer:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    buffer += chunk
        except OSError as err:
            return self._unavailable(cmd, f"unreachable ({err})")

        line = buffer.split(b"\n", 1)[0].decode("utf-8", "replace").strip()
        if not line:
            return self._unavailable(cmd, "connection closed without a reply")

        try:
            reply = json.loads(line)
        except ValueError as err:
            return self._unavailable(cmd, f"malformed reply ({err})")

        if not isinstance(reply, dict):
            return self._unavailable(cmd, f"reply is not an object ({reply!r})")

        return reply

    # Claim the bus.  Raises BusBusy if pmcapture says someone else has it,
    # and BusUnavailable if a socket is there but the arbiter said nothing
    # usable; either way the caller must not touch the bus.
    def acquire(self):
        with self._mutex:
            if self._depth > 0:
                self._depth += 1
                return

            # Only the no-socket case returns here, and it is the one case
            # that may proceed unarbitrated.
            reply = self._exchange("acquire")
            if reply is None:
                self._depth = 1
                self._granted = False
                return

            if not reply.get("ok", False):
                raise BusBusy(reply.get("error") or "pmcapture refused the I2C bus")

            self._depth = 1
            self._granted = True

    # Give the bus back.  Safe to call when the window was never granted.
    def release(self):
        with self._mutex:
            if self._depth == 0:
                return

            self._depth -= 1
            if self._depth > 0:
                return

            if self._granted:
                # Best effort, unlike acquire: the bus work is already
                # finished, so failing the caller here would report an error
                # for an operation that succeeded.  A release that never
                # lands is cleared by the next one, by a daemon restart, or
                # by the daemon reclaiming the window when this process
                # exits.
                try:
                    self._exchange("release")
                except BusUnavailable as err:
                    self._logger.warning("%s", err)
                self._granted = False

    # Hold the bus for the duration of the caller's with statement.
    #
    # contextlib.contextmanager turns this generator into a context manager.
    # The code before the yield runs on entry, the body of the caller's with
    # statement runs in place of the yield, and the code after it runs on
    # exit.  Because release() sits in a finally, the window is handed back
    # on every exit path, including an exception or an early return from the
    # body, so a caller cannot leak it.
    #
    # A BusBusy or BusUnavailable from acquire() is raised before the try is
    # entered, so the body never runs and nothing is released.
    @contextlib.contextmanager
    def window(self):
        self.acquire()
        try:
            yield
        finally:
            self.release()


bus_lock = BusLock()
