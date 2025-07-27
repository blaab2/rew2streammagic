"""
Main entry point for parsing a Room EQ Wizard (REW) equalizer description file
and extracting the first seven equalizer band settings.
"""

import sys
import re
import asyncio
import argparse
from pathlib import Path
from aiohttp import ClientSession
from aiostreammagic import StreamMagicClient, EQBand, UserEQ, EQFilterType, Info
from packaging.version import Version


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
    parser = argparse.ArgumentParser(
        description="Parse REW equalizer file and apply settings to StreamMagic device"
    )
    parser.add_argument("eq_file", help="Path to REW equalizer file")
    parser.add_argument(
        "--ip",
        default="192.168.1.29",
        help="IP address of StreamMagic device (default: 192.168.1.29)"
    )
    
    args = parser.parse_args()
    
    eq_file = Path(args.eq_file)
    if not eq_file.exists():
        print(f"File not found: {eq_file}")
        sys.exit(1)
    
    user_eq = parse_eq_file(eq_file)
    if not user_eq.bands:
        print("No equalizer bands found in the file.")
        sys.exit(1)
    
    print("First 7 Equalizer Bands:")
    for band in user_eq.bands:
        print(f"Band {band.index}: Freq={band.freq}Hz, Gain={band.gain}dB, Q={band.q}")

    async with ClientSession() as session:
        client = StreamMagicClient(args.ip, session=session)
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
