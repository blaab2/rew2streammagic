"""
Main entry point for parsing a Room EQ Wizard (REW) equalizer description file
and extracting the first seven equalizer band settings.
"""

import sys
import re
import asyncio
import ipaddress
from pathlib import Path
from aiostreammagic import StreamMagicClient, EQBand, UserEQ, EQFilterType, Info
from packaging.version import Version


def validate_ip_address(ip_str):
    """
    Validate that the provided string is a valid IP address.

    Args:
        ip_str (str): The IP address string to validate

    Returns:
        str: The validated IP address

    Raises:
        ValueError: If the IP address is invalid
    """
    try:
        # This will validate both IPv4 and IPv6 addresses
        validated_ip = ipaddress.ip_address(ip_str)
        return str(validated_ip)
    except ValueError as e:
        raise ValueError(f"Invalid IP address '{ip_str}': {e}")


def parse_eq_file(file_path):
    bands = []
    filter_map = {
        "LS": "LOWSHELF",
        "PK": "PEAKING",
        "HS": "HIGHSHELF",
        "LP": "LOWPASS",
        "HP": "HIGHPASS",
    }
    band_pattern = re.compile(
        r"^Filter\s+(\d+):\s+ON\s+([A-Z]+)\s+Fc\s+([\d.]+)\s*Hz(?:\s+Gain\s+([\-\d.]+)\s*dB)?(?:\s+Q\s+([\d.]+))?"
    )
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = band_pattern.match(line.strip())
            if match:
                band_num = int(match.group(1)) - 1  # zero-based index
                filter_type = match.group(2)
                freq = float(match.group(3))
                gain = float(match.group(4)) if match.group(4) is not None else None
                q = float(match.group(5)) if match.group(5) is not None else None
                mapped_filter = filter_map.get(filter_type, filter_type)
                band = EQBand(
                    index=band_num,
                    filter=EQFilterType[mapped_filter],
                    freq=int(freq),
                    gain=gain,
                    q=q,
                )
                bands.append(band)
                if len(bands) == 7:
                    break
    return UserEQ(bands=bands)


async def main():
    if len(sys.argv) < 3:
        print("Usage: python -m rew2streammagic.main <path_to_eq_file> <ip_address>")
        sys.exit(1)

    eq_file = Path(sys.argv[1])
    if not eq_file.exists():
        print(f"File not found: {eq_file}")
        sys.exit(1)

    # Validate IP address
    try:
        ip_address = validate_ip_address(sys.argv[2])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    user_eq = parse_eq_file(eq_file)
    if not user_eq.bands:
        print("No equalizer bands found in the file.")
        sys.exit(1)
    print("First 7 Equalizer Bands:")
    for band in user_eq.bands:
        print(f"Band {band.index}: Freq={band.freq}Hz, Gain={band.gain}dB, Q={band.q}")

    print(f"Connecting to StreamMagic device at {ip_address}...")
    async with StreamMagicClient(ip_address) as client:
        await client.connect()
        info: Info = await client.get_info()

        print(f"API: {info.api_version}")
        if Version(info.api_version) >= Version("1.9"):
            # Example of setting equalizer band gain and frequency
            # await client.set_equalizer_band_gain(0, 3.0)
            # await client.set_equalizer_band_frequency(0, 100)
            await client.set_equalizer_params(user_eq)


if __name__ == "__main__":
    asyncio.run(main())
