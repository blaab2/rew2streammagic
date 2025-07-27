#!/usr/bin/env python3
"""
IPv6 Examples Demonstration

This script demonstrates various IPv6 address formats that are supported
by the rew2streammagic tool for connecting to StreamMagic devices.
"""

import ipaddress


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


def main():
    print("rew2streammagic IPv6 Address Support Demonstration")
    print("=" * 60)
    print()

    # IPv6 examples from the README
    ipv6_examples = [
        ("::1", "IPv6 localhost (compressed notation)"),
        ("fe80::1234:5678:abcd:ef01", "IPv6 link-local address"),
        ("2001:db8::1", "IPv6 global unicast address (compressed notation)"),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", "IPv6 full notation"),
        ("::ffff:192.168.1.1", "IPv4-mapped IPv6 address"),
        ("fe80::1%eth0", "IPv6 with zone identifier (for link-local addresses)"),
    ]

    print("All of the following IPv6 address formats are supported:\n")

    for ip_addr, description in ipv6_examples:
        try:
            validated = validate_ip_address(ip_addr)
            print(f"✓ {ip_addr:<35} -> {validated}")
            print(f"  {description}")
            print()
        except ValueError as e:
            print(f"✗ {ip_addr:<35} -> ERROR: {e}")
            print()

    print("Usage Example Commands:")
    print("-" * 30)
    for ip_addr, description in ipv6_examples:
        print(
            f"poetry run python -m rew2streammagic.main example_data/default.txt {ip_addr}"
        )

    print()
    print("Note: These examples demonstrate IP address validation.")
    print(
        "Actual device connection requires a valid StreamMagic device at the specified address."
    )


if __name__ == "__main__":
    main()
