#!/usr/bin/env python3
# Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Short status text for status.json and "pmcapture status" output.
# Used by capture_daemon and the CLI.

from __future__ import annotations


# Return whether the GPIO level matches the configured active level.
def trigger_condition_met(trigger: dict | None) -> bool | None:
    if not trigger:
        return None
    level = trigger.get("level")
    if level is None:
        return None
    active = str(trigger.get("active") or "high").lower()
    if active == "high":
        return level == 1
    if active == "low":
        return level == 0
    return None


# Summarize armed vs sampling state for status output.
def build_capture_visibility(
    *,
    state: str,
    session: dict | None,
    trigger: dict | None,
    error: str | None = None,
) -> dict:
    armed = trigger is not None
    sampling_active = state == "running" and session is not None

    if state == "error":
        detail = error or "see daemon logs"
        return {
            "sampling_active": False,
            "armed": armed,
            "phase": "error",
            "summary": f"ERROR: not sampling ({detail})",
        }

    if sampling_active:
        if trigger and trigger.get("gpio_gated"):
            return {
                "sampling_active": True,
                "armed": armed,
                "phase": "running_gpio_window",
                "summary": "active — sampling rails (GPIO capture window open)",
            }
        client = format_client_label((session or {}).get("client"))
        return {
            "sampling_active": True,
            "armed": armed,
            "phase": "running_manual",
            "summary": f"active — sampling rails ({client} session)",
        }

    if armed or state == "armed":
        condition = trigger_condition_met(trigger)
        if condition is True:
            return {
                "sampling_active": False,
                "armed": True,
                "phase": "armed_trigger_met",
                "summary": (
                    "armed — trigger condition met, not sampling "
                    "(waiting for inactive -> active transition to sample)"
                ),
            }
        if condition is False:
            return {
                "sampling_active": False,
                "armed": True,
                "phase": "armed_waiting",
                "summary": (
                    "armed — monitoring GPIO, not sampling "
                    "(trigger condition not met)"
                ),
            }
        return {
            "sampling_active": False,
            "armed": True,
            "phase": "armed_waiting",
            "summary": "armed — monitoring GPIO, not sampling (trigger level unknown)",
        }

    return {
        "sampling_active": False,
        "armed": False,
        "phase": "idle",
        "summary": "idle — not armed, not sampling",
    }


# Return user-facing client name (CLI, BEAM, and GPIO are capitalized).
def format_client_label(client: str | None) -> str:
    if not client or client.lower() == "cli":
        return "CLI"
    if client.lower() == "beam":
        return "BEAM"
    if client.lower() == "gpio":
        return "GPIO"
    return client


# CLI-friendly trigger condition label.
def format_trigger_condition(trigger: dict | None) -> str:
    met = trigger_condition_met(trigger)
    if met is True:
        return "met"
    if met is False:
        return "not met"
    return "unknown"
