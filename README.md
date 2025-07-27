# rew2streammagic

rew2streammagic is a Python tool to parse Room EQ Wizard (REW) equalizer description files (Equalizer APO file format) and apply the extracted equalizer settings to Cambridge Audio StreamMagic devices.

## Features

- Parse REW filter files and extract the first seven equalizer bands
- Supports various filter types (PEAKING, LOWSHELF, HIGHSHELF, LOWPASS, HIGHPASS)
- Maps REW filter types to StreamMagic-compatible types
- Communicates with StreamMagic devices to set user EQ parameters
- **Full IPv4 and IPv6 address support** for device connectivity

## IP Address Support

The tool supports both IPv4 and IPv6 addresses for connecting to StreamMagic devices:

- **IPv4**: Standard dotted decimal notation (e.g., `192.168.1.29`, `10.0.0.100`)
- **IPv6**: All standard IPv6 formats including:
  - Compressed notation (e.g., `::1`, `2001:db8::1`)
  - Full notation (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`)
  - Link-local addresses (e.g., `fe80::1234:5678:abcd:ef01`)
  - IPv4-mapped IPv6 addresses (e.g., `::ffff:192.168.1.1`)
  - Zone identifiers for link-local addresses (e.g., `fe80::1%eth0`)

All IP addresses are validated before attempting connection to ensure proper format.

## Usage

1. Prepare a REW filter file (see `example_data/` for samples).

1. Install dependencies

    ```sh
    poetry install
    ```

1. Run the tool:

    ```sh
    poetry run python -m rew2streammagic.main <path_to_eq_file> <ip_address>
    ```

1. The tool will parse the file and send the EQ settings to your StreamMagic device at the specified IP address, if it is supported by the API version.

## Example

See the `example_data/` folder for sample input files.

For a comprehensive demonstration of IPv6 address support, run:
```sh
python3 examples/ipv6_demonstration.py
```

### Usage Examples

#### IPv4 Examples
```sh
# Connect to a StreamMagic device at IP address 192.168.1.29
poetry run python -m rew2streammagic.main example_data/default.txt 192.168.1.29

# Connect to a device at a different IP address
poetry run python -m rew2streammagic.main example_data/peaking.txt 10.0.0.100

# Connect to a device on localhost
poetry run python -m rew2streammagic.main example_data/filter_types.txt 127.0.0.1
```

#### IPv6 Examples
```sh
# IPv6 localhost (compressed notation)
poetry run python -m rew2streammagic.main example_data/default.txt ::1

# IPv6 link-local address
poetry run python -m rew2streammagic.main example_data/peaking.txt fe80::1234:5678:abcd:ef01

# IPv6 global unicast address (compressed notation)
poetry run python -m rew2streammagic.main example_data/filter_types.txt 2001:db8::1

# IPv6 full notation
poetry run python -m rew2streammagic.main example_data/default.txt 2001:0db8:85a3:0000:0000:8a2e:0370:7334

# IPv4-mapped IPv6 address
poetry run python -m rew2streammagic.main example_data/peaking.txt ::ffff:192.168.1.1

# IPv6 with zone identifier (for link-local addresses)
poetry run python -m rew2streammagic.main example_data/filter_types.txt fe80::1%eth0
```

## Requirements

> [!WARNING]
> The changes required for equalizer support are not yet released in aiostreammagic and are only available in this [feature branch](https://github.com/Solmath/aiostreammagic/tree/feature/add-eq-support)

- Python 3.11+
- [aiostreammagic](https://github.com/noahhusby/aiostreammagic)
- poetry (for development)
