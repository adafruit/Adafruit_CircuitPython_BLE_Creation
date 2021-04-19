# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""This example scans for creation advertisements and prints them out."""

import adafruit_ble
import adafruit_ble_creation

ble = adafruit_ble.BLERadio()

print("scanning")
# By providing Advertisement as well we include everything, not just specific advertisements.
for advert in ble.start_scan(adafruit_ble_creation.Creation, interval=0.1):
    creation_name = None
    for c in adafruit_ble_creation.creation_ids:
        cid = adafruit_ble_creation.creation_ids[c]
        if cid == advert.creation_id:
            creation_name = c
            break
    print(advert.address, creation_name)
