"""MIDI input handler using mido + python-rtmidi."""

from PySide6.QtCore import QObject, Signal
import mido


class MIDIListener(QObject):
    note_on = Signal(int, int)  # pitch, velocity
    note_off = Signal(int)  # pitch

    def __init__(self):
        super().__init__()
        self.inport = None
        self.open_port()

    def open_port(self):
        """Open the first MIDI port matching 'Komplete Kontrol'."""
        for port_name in mido.get_input_names():
            if "Komplete Kontrol" in port_name:
                try:
                    self.inport = mido.open_input(port_name)
                    return True
                except Exception:
                    return False
        return False

    def is_connected(self):
        """Check if MIDI port is open."""
        return self.inport is not None

    def get_available_ports(self):
        """List all MIDI input ports."""
        return mido.get_input_names()

    def poll(self):
        """Poll for MIDI messages and emit signals."""
        if not self.inport:
            return

        for msg in self.inport.iter_pending():
            if msg.type == "note_on":
                self.note_on.emit(msg.note, msg.velocity)
            elif msg.type == "note_off":
                self.note_off.emit(msg.note)

    def close(self):
        """Close MIDI port."""
        if self.inport:
            self.inport.close()
