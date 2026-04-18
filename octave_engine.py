from collections import defaultdict
from hid_driver import hid_driver
from logger import logger

class OctaveEngine:
    """Pitch-class tracking and lighting logic."""

    MIDI_MIN = 36
    MIDI_MAX = 96

    def __init__(self, color='#FF0000'):
        self.pitch_class_counts = defaultdict(int)
        self.color = color

    def note_on(self, pitch):
        """Handle note-on event."""
        if not (self.MIDI_MIN <= pitch <= self.MIDI_MAX):
            logger.warning(f"Pitch {pitch} outside range")
            return

        pitch_class = pitch % 12
        self.pitch_class_counts[pitch_class] += 1

        pitches_to_light = [
            p for p in range(self.MIDI_MIN, self.MIDI_MAX + 1)
            if p % 12 == pitch_class
        ]
        hid_driver.set_keys_lit(pitches_to_light, self.color)
        logger.debug(f"Lit pitch class {pitch_class}: {pitches_to_light}")

    def note_off(self, pitch):
        """Handle note-off event."""
        if not (self.MIDI_MIN <= pitch <= self.MIDI_MAX):
            return

        pitch_class = pitch % 12
        self.pitch_class_counts[pitch_class] -= 1

        if self.pitch_class_counts[pitch_class] <= 0:
            self.pitch_class_counts[pitch_class] = 0
            pitch_class_keys = [
                p for p in range(self.MIDI_MIN, self.MIDI_MAX + 1)
                if p % 12 == pitch_class
            ]
            hid_driver.set_keys_with_colors(
                {p: '#000000' for p in pitch_class_keys}
            )
            logger.debug(f"Extinguished pitch class {pitch_class}")

    def set_color(self, color):
        """Change highlight color."""
        self.color = color

    def shutdown(self):
        """Clear all lights on shutdown."""
        hid_driver.clear_all()
        self.pitch_class_counts.clear()

octave_engine = OctaveEngine()
