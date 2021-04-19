# SPDX-FileCopyrightText: Copyright (c) 2021 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""This example broadcasts out the creation id based on the CircuitPython machine
   string."""

import time
import os
import adafruit_ble
import adafruit_ble_creation

cid = adafruit_ble_creation.creation_ids[os.uname().machine]

ble = adafruit_ble.BLERadio()
print(ble.name)
advert = adafruit_ble_creation.Creation(creation_id=cid)
print(bytes(advert), len(bytes(advert)))

ble.start_advertising(advert)
time.sleep(120)
ble.stop_advertising()
