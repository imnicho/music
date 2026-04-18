import sys
import atexit
import signal
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

from gui import MainWindow
from midi_listener import midi_listener
from octave_engine import octave_engine
from hid_driver import hid_driver
from logger import logger

class OctaveLightsApp:
    """Main application controller."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self._enforce_single_instance()
        self._setup_exception_handler()
        self._setup_cleanup()

    def _enforce_single_instance(self):
        """Prevent multiple instances via Windows mutex."""
        import uuid
        self.mutex_name = "OctaveLights_" + str(uuid.uuid4())[:8]
        try:
            import ctypes
            self.mutex = ctypes.windll.kernel32.CreateMutexW(
                None, True, self.mutex_name
            )
            if ctypes.windll.kernel32.GetLastError() == 183:
                QMessageBox.warning(
                    None,
                    "OctaveLights",
                    "OctaveLights is already running."
                )
                sys.exit(1)
        except Exception as e:
            logger.warning(f"Could not enforce single instance: {e}")

    def _setup_exception_handler(self):
        """Global exception handler."""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.error(
                f"Uncaught exception: {exc_type.__name__}: {exc_value}",
                exc_info=(exc_type, exc_value, exc_traceback)
            )
            QMessageBox.critical(
                self.window,
                "Error",
                f"An error occurred: {exc_value}\n\nSee logs for details."
            )

        sys.excepthook = handle_exception

    def _setup_cleanup(self):
        """Ensure cleanup on all exit paths."""
        def cleanup():
            logger.info("Shutting down...")
            midi_listener.stop()
            octave_engine.shutdown()
            hid_driver.close()
            logger.info("Shutdown complete")

        atexit.register(cleanup)
        self.app.aboutToQuit.connect(cleanup)

        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: sys.exit(0))

    def run(self):
        """Launch the app."""
        logger.info("Starting OctaveLights")
        self.window = MainWindow()
        self.window.show()

        midi_listener.note_on.connect(octave_engine.note_on)
        midi_listener.note_off.connect(octave_engine.note_off)
        midi_listener.start()

        if not hid_driver.is_connected():
            self.window.update_status("HID device not found")
        else:
            self.window.update_status("Connected")

        sys.exit(self.app.exec())

if __name__ == '__main__':
    app = OctaveLightsApp()
    app.run()
