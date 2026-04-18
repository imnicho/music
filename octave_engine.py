"""Core logic for pitch-class tracking and lighting coordination."""


class OctaveEngine:
    def __init__(self, hid_driver):
        """Initialize with pitch-class tracking (36-96 MIDI range)."""
        self.hid_driver = hid_driver
        self.pitch_map = {}  # pitch -> count (reference counting)
        self.default_color = "white"
        self.highlight_pressed = False
        self.highlight_color = "cyan"

    def on_note_on(self, pitch, velocity=100):
        """Handle note-on: light all octave-siblings."""
        if pitch < 36 or pitch > 96:
            return

        pitch_class = pitch % 12
        if pitch not in self.pitch_map:
            self.pitch_map[pitch] = 0
        self.pitch_map[pitch] += 1

        to_light = [p for p in range(36, 97) if p % 12 == pitch_class]

        if self.highlight_pressed:
            colors = {pitch: self.highlight_color}
            for p in to_light:
                if p != pitch:
                    colors[p] = self.default_color
            self.hid_driver.set_keys_with_colors(colors)
        else:
            self.hid_driver.set_keys_lit(to_light, self.default_color)

    def on_note_off(self, pitch):
        """Handle note-off: decrement reference count, update lights."""
        if pitch < 36 or pitch > 96 or pitch not in self.pitch_map:
            return

        self.pitch_map[pitch] -= 1
        if self.pitch_map[pitch] <= 0:
            del self.pitch_map[pitch]

        pitch_class = pitch % 12
        active_pitches = [p for p in self.pitch_map if p % 12 == pitch_class]

        if not active_pitches:
            to_dark = [p for p in range(36, 97) if p % 12 == pitch_class]
            self.hid_driver.set_keys_lit(to_dark, "off")
        else:
            to_light = [p for p in range(36, 97) if p % 12 == pitch_class]
            if self.highlight_pressed:
                colors = {}
                for p in to_light:
                    colors[p] = (
                        self.highlight_color
                        if p in self.pitch_map
                        else self.default_color
                    )
                self.hid_driver.set_keys_with_colors(colors)
            else:
                self.hid_driver.set_keys_lit(to_light, self.default_color)

    def set_color(self, color_name):
        """Set the default lighting color."""
        self.default_color = color_name

    def set_highlight_pressed(self, enabled, color):
        """Enable/disable highlight for pressed key with secondary color."""
        self.highlight_pressed = enabled
        self.highlight_color = color

    def shutdown(self):
        """Clear all lights on shutdown."""
        self.hid_driver.clear_all()
