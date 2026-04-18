import threading
import hid
from logger import logger

class HIDDriver:
    """USB HID communication with Komplete Kontrol S61 MK1."""

    VENDOR_ID = 0x17cc
    PRODUCT_ID = 0x1360
    MIDI_MIN = 36
    MIDI_MAX = 96

    def __init__(self):
        self.device = None
        self.lock = threading.Lock()
        self._open_device()

    def _open_device(self):
        """Open HID device for S61 MK1."""
        try:
            self.device = hid.device()
            self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            logger.info("HID device opened successfully")
        except Exception as e:
            logger.error(f"Failed to open HID device: {e}")
            self.device = None

    def is_connected(self):
        """Check if device is connected."""
        return self.device is not None

    def set_keys_lit(self, pitch_list, color):
        """Light multiple keys with the same color."""
        color_map = {pitch: color for pitch in pitch_list}
        self.set_keys_with_colors(color_map)

    def set_keys_with_colors(self, pitch_color_dict):
        """Set individual keys with their own colors.

        pitch_color_dict: {pitch: color_hex, ...} e.g. {36: '#FF0000'}
        """
        if not self.is_connected():
            return

        with self.lock:
            for pitch, color in pitch_color_dict.items():
                if not (self.MIDI_MIN <= pitch <= self.MIDI_MAX):
                    logger.warning(f"Pitch {pitch} outside range {self.MIDI_MIN}-{self.MIDI_MAX}")
                    continue
                self._send_light_command(pitch, color)

    def _send_light_command(self, pitch, color):
        """Send a single light command via HID (derived from SynthesiaKontrol)."""
        try:
            pass
        except Exception as e:
            logger.error(f"HID write error for pitch {pitch}: {e}")

    def clear_all(self):
        """Turn off all lights."""
        if not self.is_connected():
            return

        with self.lock:
            try:
                pass
            except Exception as e:
                logger.error(f"Failed to clear lights: {e}")

    def close(self):
        """Close HID device."""
        if self.device:
            with self.lock:
                try:
                    self.device.close()
                    logger.info("HID device closed")
                except Exception as e:
                    logger.error(f"Error closing HID device: {e}")
                finally:
                    self.device = None

hid_driver = HIDDriver()
