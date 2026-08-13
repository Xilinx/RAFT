# pmcapture — RAFT INA power capture (daemon + CLI)

Short guide; canonical option text is in **`pmcapture.1`** (installed as **`man pmcapture`** when the
`man` package is present). Many SC images omit `man` — use **`pmcapture --help`**, this file, or
**`less /usr/share/raft/examples/python/pmcapture/pmcapture.1`**.

## What it does

`pmcapture` drives the System Controller INA power sampler using RAFT board JSON
and sensor drivers. **`pmcapture.service`** runs an idle supervisor after boot
(no I2C until a session starts). **`start`** sends work to the daemon; only one
session at a time. Board layout comes from  
`xserver/raft_services/power_management/board/<BOARD>.json` (board identity from
`/bin/sc-board-id` when available, otherwise FRU EEPROM — same logic as
raft-startup, including revision-specific JSON such as `VEK386-A1.json`).

## Install (System Controller)

Yocto: enable **`raftstartupsc`** for the RAFT recipe  
(`PACKAGECONFIG:append = " raftstartupsc"`).  
From sources: **`make install STARTUPSC=enabled`**.

That installs **`pmcapture`**, **`pmcapture.service`**, and the Python modules
under `/usr/share/raft/examples/python/pmcapture/`.

## Commands

| Command | Role |
|--------|------|
| **`daemon`** | Foreground supervisor; used by systemd. Unix socket + `status.json`. |
| **`start`** | Begin capture in the daemon; CLI exits after the request. |
| **`stop`** | End active session (returns to **`armed`** if GPIO trigger still armed). |
| **`status`** | Idle / armed / running / error, `capture:` summary, session metadata. Use **`-j`** / **`--json`** for machine-readable output. |
| **`ping`** | Check control socket. |
| **`arm`** | Arm GPIO-triggered file capture (see below). |
| **`disarm`** | Stop trigger monitor; return to idle. |

CLI failures print a single-line message prefixed with **`ERROR:`** on stderr.

## GPIO-triggered capture (`arm` / `disarm`)

For offline file capture gated by a DUT GPIO line (interrupt-driven via
**libgpiod v2**). While **armed**, manual **`start`** is rejected.

```bash
# Arm from CLI flags only
pmcapture arm --gpio SYSCTRL_GPI4 --rails all --file-format csv
pmcapture status
pmcapture disarm
```

Board-specific device-tree labels (e.g. legacy readback names) resolve when
present in `gpioinfo` or via libgpiod on `/dev/gpiochip*`.

```bash
# GPIO trigger profile — save as /data/pmcapture/trigger_capture.json
cat <<'EOF' > /data/pmcapture/trigger_capture.json
{
  "rails": ["VCCINT", "VCCAIE"],
  "rate_hz": 20,
  "output": "file",
  "file_format": "csv",
  "trigger": {
    "gpio": "SYSCTRL_GPI4",
    "active": "high",
    "debounce_ms": 0
  }
}
EOF

# Arm from JSON; CLI flags override unset fields
pmcapture arm --capture-config /data/pmcapture/trigger_capture.json
pmcapture arm --capture-config /data/pmcapture/trigger_capture.json --file-format jsonl
pmcapture disarm
```

Each GPIO assert→deassert window writes a separate file under
`/data/pmcapture/` (suffix `gpioN`).

While **armed** the daemon holds the trigger line (`consumer=pmcapture-trigger`).
GPIO **assert** (active level) starts sampling; **deassert** stops the window.
No I2C traffic until a window is active.

## `start` options (overview)

| Flag | Meaning |
|------|---------|
| **`-r` / `--rails`** | Default **`all`** (every **POWER SENSORS** entry). Comma-separated **POWER DOMAIN** names (e.g. `LPD,AIE`) or **POWER SENSOR** names (e.g. `VCCINT_1,VCC_AIE_1`). Legacy values `power_domains` / `power_sensors` are treated as **`all`**. |
| **`-c` / `--capture-config`** | Optional JSON (see below); CLI overrides unset fields. |
| **`-o` / `--output`** | `file` (default) or `tcp` (newline-delimited JSON stream; daemon implements TCP — BEAM dashboard consumer tracked in SSW-18337). |
| **`-t` / `--rate`** | Sample rate Hz (0.1–50, default 20). |
| **`-d` / `--duration`** | Seconds; `0` = until **`stop`** or daemon exit. |
| **`-f` / `--output-file`** | File path; if omitted, auto name under `/data/pmcapture/` (`capture_<board>_<timestamp>.<ext>` or `…_gpioN.<ext>`). |
| **`-F` / `--file-format`** | `jsonl` (default) or `csv`. |
| **`-H` / `--host`** | TCP bind address (default `0.0.0.0`). |
| **`-p` / `--port`** | TCP port (default **18094**). |
| **`-u` / `--client`** | Session owner label stored as `cli` (default), `beam`, or `gpio`; **`pmcapture status`** displays **CLI**, **BEAM**, or **GPIO**. |

## Paths

| Path | Purpose |
|------|---------|
| `/usr/bin/pmcapture` | CLI (symlink into install tree). |
| `/usr/share/raft/examples/python/pmcapture/` | Program modules. |
| `/run/pmcapture/control.sock` | Control socket (one JSON line per message). |
| `/run/pmcapture/status.json` | Daemon + session state. |
| `/data/pmcapture/` | Default directory for auto-generated capture files. |
| `/etc/systemd/system/pmcapture.service` | systemd unit. |

## Output formats

- **`jsonl`**: First line catalog (`type=catalog`); following lines one JSON object per sample (`ts`, `rails` V/I/W, board, rate). Inspect with standard tools (`less`, `jq`, etc.) after copy off the SC.
- **`csv`**: Header with `ts`, `rate_hz`, then `<RAIL>_V` / `_I` / `_W` columns; one row per sample.

## Capture config JSON (`--capture-config`)

JSON may set: `rails`, `rate_hz`, `duration_s`, `output`, `output_file`,
`file_format`, and (for GPIO arm) `trigger`.

**`rails`** is either:
- a **string selector** (same as CLI `--rails`: `all`, a domain name, or comma-separated names), or
- an **array** of explicit rail names to trim the active pool.

When both CLI and JSON supply options, CLI values override JSON **only for fields you pass on the command line**. Because **`--rails` defaults to `all`**, a JSON string selector such as `"rails": "LPD"` is not applied unless you omit `-r` from a wrapper script or pass `-r LPD` explicitly. Prefer a **`rails` array** in JSON to subset rails without relying on CLI merge.

Deprecated: **`rails_pool`** / **`rails_selection`** are still accepted as aliases for a string **`rails`** selector.

```bash
# Rail subset (60 s, CSV) — save as /data/pmcapture/subset.json
cat <<'EOF' > /data/pmcapture/subset.json
{
  "rails": ["VCCINT_1", "VCCINT_2", "VCC_AIE_1", "VCC_AIE_2"],
  "rate_hz": 20,
  "duration_s": 60,
  "output": "file",
  "file_format": "csv"
}
EOF

# All sensors, open-ended until stop — save as /data/pmcapture/open_ended.json
cat <<'EOF' > /data/pmcapture/open_ended.json
{
  "rails": "all",
  "rate_hz": 20,
  "duration_s": 0,
  "output": "file",
  "file_format": "jsonl"
}
EOF

pmcapture start --duration 60 --capture-config /data/pmcapture/subset.json
```

## Example shell commands

```bash
# Daemon and session status
pmcapture status
pmcapture status --json
pmcapture ping

# Timed file capture (120 s, LPD domain rails, CSV)
sudo pmcapture start --duration 120 --output-file /data/pmcapture.out \
  --file-format csv --rails LPD

# Named rail subset for 60 s
sudo pmcapture start \
  --rails VCCINT_1,VCCINT_2,VCCINT_3,VCCINT_4,VCC_AIE_1,VCC_AIE_2,VCC_AIE_3,VCC_AIE_4 \
  --duration 60 --file-format csv

# Capture from JSON profile
sudo pmcapture start --duration 60 --capture-config /data/pmcapture/subset.json

# TCP streaming (BEAM dashboard consumer tracked in SSW-18337)
sudo pmcapture start --output tcp --port 18094 --rails all --client beam
pmcapture stop
```

## Exit status

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Failure — message on stderr begins with **`ERROR:`** |
| 2 | Invalid usage — stderr message begins with **`ERROR:`** |
| 130 | Interrupted in **`daemon`** foreground mode |

## See also

- **`pmcapture.1`** / **`man pmcapture`** — canonical option text and **EXAMPLES** layout (when `man` is installed).
- **`pmcapture --help`** — quick option summary on any SC image.
- **`pmcapture.service`** unit under `/etc/systemd/system/` (no separate man page today).
- Board JSON: `/usr/share/raft/xserver/raft_services/power_management/board/`.
