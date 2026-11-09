# 0.2.0-dev engineering snapshot

These images compile the revision0.2 custom INA228 board design with **public test-only Thread/API/OTA fixtures**. DO NOT DEPLOY them to a real network. Rebuild with owner-local independent secrets before flashing. No image has been flashed to or tested on physical hardware. Revision0.1 images are incompatible with this board.

`checksums.json` records exact firmware source-file hashes, build configuration hashes, timestamps, sizes and SHA256 values. Factory images include the bootloader/partitions; OTA images are application updates for an already provisioned matching device. Confirm the actual serial port and flash offset with the pinned ESPHome toolchain; do not guess offsets from another ESP32 model.

This directory is a versioned development snapshot, not production approval or a published GitHub tag/release. Electrical stability, sensor accuracy, hardware faults, RF/OTA recovery, battery autonomy, enclosure/weather and structural mounting still require the recorded qualification procedures.
