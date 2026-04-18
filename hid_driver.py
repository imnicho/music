"""USB HID communication with S61 MK1 via hidapi."""

import threading
import queue

try:
    import hidapi
except ImportError:
    hidapi = None


class HIDDriver:
    VENDOR_ID = 0x17CC
    PRODUCT_ID = 0x1360

    def __init__(self):
        """Initialize HID device and worker thread."""
        self.device = None
        self.cmd_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self.open()

    def open(self):
        """Open the S61 MK1 device."""
        if not hidapi:
            return False
        try:
            self.device = hidapi.Device(self.VENDOR_ID, self.PRODUCT_ID)
            return True
        except Exception:
            return False

    def is_connected(self):
        """Check if device is open."""
        return self.device is not None

    def _worker(self):
        """Worker thread to serialize all HID I/O."""
        while True:
            cmd = self.cmd_queue.get()
            if cmd is None:
                break
            try:
                if cmd[0] == "set_keys":
                    self._do_set_keys(cmd[1], cmd[2])
                elif cmd[0] == "set_colors":
                    self._do_set_colors(cmd[1])
                elif cmd[0] == "clear":
                    self._do_clear()
            except Exception:
                pass

    def set_keys_lit(self, pitch_list, color):
        """Queue command to light specific pitches with one color."""
        self.cmd_queue.put(("set_keys", pitch_list, color))

    def set_keys_with_colors(self, pitch_color_dict):
        """Queue command to light pitches with individual colors."""
        self.cmd_queue.put(("set_colors", pitch_color_dict))

    def clear_all(self):
        """Queue command to turn off all lights."""
        self.cmd_queue.put(("clear",))

    def _do_set_keys(self, pitch_list, color):
        """Internal: send HID report to light keys.

        Reference: SynthesiaKontrol for MK1 Light Guide protocol byte layout.
        TODO: Implement actual MK1 protocol based on SynthesiaKontrol.
        """
        if not self.device:
            return

    def _do_set_colors(self, pitch_color_dict):
        """Internal: send HID report with per-key colors.

        TODO: Implement actual MK1 protocol based on SynthesiaKontrol.
        """
        if not self.device:
            return

    def _do_clear(self):
        """Internal: turn off all lights.

        TODO: Implement actual MK1 protocol based on SynthesiaKontrol.
        """
        if not self.device:
            return

    def close(self):
        """Shutdown worker and close device."""
        self.cmd_queue.put(None)
        if self.device:
            self.device.close()
