import threading
import mido
from PySide6.QtCore import QObject, Signal
from logger import logger

class MIDIListener(QObject):
    """MIDI input handler for Komplete Kontrol S61."""

    note_on = Signal(int)  # pitch
    note_off = Signal(int)  # pitch

    def __init__(self):
        super().__init__()
        self.port = None
        self.listening = False
        self.thread = None

    def start(self):
        """Start listening for MIDI input."""
        self.listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop listening."""
        self.listening = False
        if self.port:
            self.port.close()
        if self.thread:
            self.thread.join(timeout=2)

    def _open_port(self):
        """Open MIDI input port for S61."""
        try:
            ports = mido.get_input_names()
            for port_name in ports:
                if 'Komplete Kontrol' in port_name:
                    self.port = mido.open_input(port_name)
                    logger.info(f"MIDI port opened: {port_name}")
                    return True
            logger.warning("Komplete Kontrol MIDI port not found")
            return False
        except Exception as e:
            logger.error(f"Failed to open MIDI port: {e}")
            return False

    def _listen_loop(self):
        """Poll for MIDI messages."""
        if not self._open_port():
            return

        while self.listening:
            try:
                for msg in self.port.iter_pending():
                    if msg.type == 'note_on' and msg.velocity > 0:
                        self.note_on.emit(msg.note)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        self.note_off.emit(msg.note)
            except Exception as e:
                logger.error(f"MIDI read error: {e}")
                break

midi_listener = MIDIListener()
