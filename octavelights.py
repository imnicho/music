# MK1 HID protocol derived from:
#   https://github.com/ojacques/SynthesiaKontrol (commit 4693f85e9ff3f468da906e5b1e745096d7c6b304)
#   cross-referenced against
#   https://github.com/simonalveteg/KompleteKontrolLightGuide (commit 8b0953a1067a99d55c719a878ffc0a4e58fc334f)
# Report ID 0x82, 3 bytes (R,G,B) per key, init handshake 0xa0 0x00 0x00.

import atexit
import logging
import logging.handlers
import os
import signal
import sys
import threading
import time

import hid
import mido

VID = 0x17CC
PID = 0x1360
LOW_PITCH = 36
HIGH_PITCH = 96
KEY_COUNT = 61
HID_REPORT_ID = 0x82
INIT_REPORT = [0xA0, 0x00, 0x00]
COLOR_ON = (0xFF, 0xFF, 0xFF)
COLOR_OFF = (0x00, 0x00, 0x00)
MIDI_PORT_MATCH = "komplete kontrol"
RECONNECT_DELAY = 2.0

APP_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "OctaveLights")
LOG_PATH = os.path.join(APP_DIR, "octavelights.log")
PID_PATH = os.path.join(APP_DIR, "octavelights.pid")
os.makedirs(APP_DIR, exist_ok=True)

_h = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=1_048_576, backupCount=3)
_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log = logging.getLogger("octavelights")
log.setLevel(logging.INFO)
log.addHandler(_h)


def build_report(active_classes):
    payload = bytearray(KEY_COUNT * 3)
    for i, pitch in enumerate(range(LOW_PITCH, HIGH_PITCH + 1)):
        color = COLOR_ON if (pitch % 12) in active_classes else COLOR_OFF
        payload[i * 3:i * 3 + 3] = color
    return bytes([HID_REPORT_ID]) + bytes(payload)


class HidLink:
    def __init__(self):
        self.dev = None
        self.lock = threading.Lock()

    def open(self):
        with self.lock:
            if self.dev is not None:
                return
            dev = hid.device()
            dev.open(VID, PID)
            dev.set_nonblocking(1)
            dev.write(INIT_REPORT)
            self.dev = dev

    def send(self, report):
        with self.lock:
            if self.dev is not None:
                self.dev.write(report)

    def close(self):
        with self.lock:
            if self.dev is not None:
                try:
                    self.dev.close()
                except Exception:
                    pass
                self.dev = None


class Engine:
    def __init__(self, link):
        self.link = link
        self.held = {}

    def _push(self):
        self.link.send(build_report({p % 12 for p in self.held}))

    def note_on(self, pitch):
        if LOW_PITCH <= pitch <= HIGH_PITCH:
            self.held[pitch] = self.held.get(pitch, 0) + 1
            self._push()

    def note_off(self, pitch):
        if pitch in self.held:
            self.held[pitch] -= 1
            if self.held[pitch] <= 0:
                del self.held[pitch]
            self._push()

    def all_off(self):
        self.held.clear()
        try:
            self.link.send(build_report(set()))
        except Exception:
            pass


def run(engine):
    while True:
        try:
            port_name = next((n for n in mido.get_input_names() if MIDI_PORT_MATCH in n.lower()), None)
            if not port_name:
                time.sleep(RECONNECT_DELAY)
                continue
            engine.link.open()
            log.info("connected: hid=%04x:%04x midi=%s", VID, PID, port_name)
            with mido.open_input(port_name) as inp:
                for msg in inp:
                    if msg.type == "note_on" and msg.velocity > 0:
                        engine.note_on(msg.note)
                    elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                        engine.note_off(msg.note)
        except Exception:
            log.exception("midi/hid error")
            engine.link.close()
            time.sleep(RECONNECT_DELAY)


def main():
    with open(PID_PATH, "w") as f:
        f.write(str(os.getpid()))
    link = HidLink()
    engine = Engine(link)
    atexit.register(engine.all_off)
    def shutdown(signum, _frame):
        log.info("signal %d received, shutting down", signum)
        engine.all_off(); engine.link.close(); sys.exit(0)
    signal.signal(signal.SIGINT, shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, shutdown)
    log.info("octavelights starting pid=%d", os.getpid())
    run(engine)


if __name__ == "__main__":
    main()
