# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_ble_creation`
================================================================================

Friendlier device discovery using Creation IDs


* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""


import struct

from adafruit_ble.advertising import Advertisement, LazyObjectField
from adafruit_ble.advertising.standard import (
    ServiceList,
    ManufacturerData,
    ManufacturerDataField,
)
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Creation.git"

_MANUFACTURING_DATA_ADT = const(0xFF)
_ADAFRUIT_COMPANY_ID = const(0x0822)
# Color packets are 1 (and radio), broadcastnet is 3.
_DEVICE_FRIEND_DATA_ID = const(0x0004)

# pylint: disable=too-few-public-methods
class Creation(Advertisement):
    """Advertise what services that the device makes available upon connection."""

    # Prefixes that match each ADT that can carry service UUIDs.
    # This single prefix matches all color advertisements.
    match_prefixes = (
        struct.pack(
            "<BHBH",
            _MANUFACTURING_DATA_ADT,
            _ADAFRUIT_COMPANY_ID,
            struct.calcsize("<HII"),
            _DEVICE_FRIEND_DATA_ID,
        ),
    )
    manufacturer_data = LazyObjectField(
        ManufacturerData,
        "manufacturer_data",
        advertising_data_type=_MANUFACTURING_DATA_ADT,
        company_id=_ADAFRUIT_COMPANY_ID,
        key_encoding="<H",
    )
    creation_id = ManufacturerDataField(
        _DEVICE_FRIEND_DATA_ID, "<II", field_names=("creator", "creation")
    )

    services = ServiceList(standard_services=[0x02, 0x03], vendor_services=[0x06, 0x07])
    """List of services the device can provide."""

    # pylint: disable=dangerous-default-value
    def __init__(self, *, creation_id=None, services=[], entry=None):
        super().__init__()
        if entry:
            return
        if services:
            self.services.extend(services)
        self.connectable = True
        self.flags.general_discovery = True
        self.flags.le_only = True
        if creation_id:
            self.creation_id = creation_id


creation_ids = {
    "Adafruit Feather nRF52840 Express with nRF52840": (0x239A, 0x802A),
    "Adafruit CLUE nRF52840 Express with nRF52840": (0x239A, 0x8072),
    "Adafruit Circuit Playground Bluefruit with nRF52840": (0x239A, 0x8046),
}
