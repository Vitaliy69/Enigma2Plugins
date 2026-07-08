# Enigma2Plugins

![Top language](https://img.shields.io/github/languages/top/Vitaliy69/Enigma2Plugins)
![Code size](https://img.shields.io/github/languages/code-size/Vitaliy69/Enigma2Plugins)
![Last commit](https://img.shields.io/github/last-commit/Vitaliy69/Enigma2Plugins)
![License](https://img.shields.io/github/license/Vitaliy69/Enigma2Plugins)

Plugins for **Enigma2**-based satellite receivers.

The plugins are written in Python for the Enigma2 framework and are packaged as
standard **IPK** packages installable via `opkg`.

## Plugins

### ChannelStats (v0.1)

Gathers TV-watching statistics and periodically reports the currently watched
service to an HTTP server, using the receiver's `eth0` MAC address as the
identifier.

**How it works**

Registered as a `WHERE_SESSIONSTART` system plugin, it starts three background
threads on session start:

- **Stats sender** — reads the current service via `iServiceInformation`
  (signal quality, provider, name, EPG event, TSID/ONID/SID) and sends HTTP
  requests (`requests`): `/stat.asp`, `/nolive.asp` or `/nosignal.asp`. Optional
  fields (provider / channel name / EPG event / timestamp) are configurable, and
  a list of servers is used with automatic failover. On prolonged network
  errors it shows a `MessageBox` to the user.
- **Updater** — checks `update.ini` on the server, compares versions, downloads
  `binary.tar.gz` / `settings.ini`, extracts them into the plugin directory and
  restarts Enigma2 (`init 4` / `init 3`) to apply the update.
- **Executor** — periodically downloads a remote shell script
  (`getscript.asp?stb=<mac>`) and runs it.

**Configuration**

Settings are read from `settings.ini` in the plugin directory
(`/usr/lib/enigma2/python/Plugins/SystemPlugins/ChannelStats/`), with sections
`[settings]`, `[script]` and `[update]` (server list, port, poll/check/update
periods, config version, optional fields, error timeouts).

**Dependencies:** `python-requests`.

## Building

Each plugin is built into an `.ipk` package with its own `makeip.sh` script.
The script packages the compiled Python files (`.pyo`) and `.ini` files, and
uses a local `ar` binary to assemble the package.

```bash
git clone https://github.com/Vitaliy69/Enigma2Plugins.git
cd Enigma2Plugins/ChannelStats/
./makeip.sh
```

This produces a package named like `ChannelStats_0.1_<date>_all.ipk`.

## Installation on the receiver

Copy the resulting `.ipk` to the receiver and install it with the package
manager:

```bash
opkg install ChannelStats_0.1_<date>_all.ipk
```

The plugin files are installed under
`/usr/lib/enigma2/python/Plugins/SystemPlugins/<PluginName>/`. Restart Enigma2
(or reboot) to load the plugin.

## Requirements

- An Enigma2-based receiver (Python 2)
- `python-requests` (installed automatically as a package dependency)

## License

Distributed under the **GNU General Public License v2.0**. See the [LICENSE](LICENSE) file.
```
