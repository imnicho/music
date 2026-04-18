from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QColorDialog, QCheckBox, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor
from config import config
from logger import logger
from version import __version__

class MainWindow(QMainWindow):
    """PySide6 GUI for OctaveLights."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OctaveLights")
        self.setGeometry(100, 100, 500, 600)

        # Try to set icon
        try:
            self.setWindowIcon(QIcon("assets/app.ico"))
        except Exception as e:
            logger.warning(f"Could not load icon: {e}")

        self._setup_ui()

    def _setup_ui(self):
        """Build the UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("OctaveLights")
        title.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title)

        # Status
        self.status_label = QLabel("Status: Initializing...")
        layout.addWidget(self.status_label)

        # Enable/Disable toggle
        toggle_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("Enable")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.clicked.connect(self._on_toggle)
        toggle_layout.addWidget(self.toggle_btn)
        layout.addLayout(toggle_layout)

        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Color:"))
        self.color_btn = QPushButton()
        self.color_btn.setMaximumWidth(100)
        self.color_btn.clicked.connect(self._on_color_picker)
        color_layout.addWidget(self.color_btn)
        layout.addLayout(color_layout)

        # Settings checkboxes
        self.highlight_pressed = QCheckBox("Highlight pressed key differently")
        self.highlight_pressed.setChecked(
            config.get('highlight_pressed_key', True)
        )
        layout.addWidget(self.highlight_pressed)

        self.startup_checkbox = QCheckBox("Launch at startup")
        self.startup_checkbox.setChecked(config.get('launch_at_startup', False))
        layout.addWidget(self.startup_checkbox)

        # About section
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setMaximumHeight(150)
        about_text.setText(
            f"<b>OctaveLights</b> v{__version__}\n\n"
            "Illuminate octave-siblings on your Komplete Kontrol S61.\n\n"
            "<b>Note:</b> Close Komplete Kontrol software before using this app.\n\n"
            "Repository: github.com/nicho-dev/octavelights"
        )
        layout.addWidget(about_text)

        layout.addStretch()

        self._update_color_display()

    def _on_toggle(self):
        """Handle enable/disable toggle."""
        state = "Enabled" if self.toggle_btn.isChecked() else "Disabled"
        logger.info(f"Toggle: {state}")

    def _on_color_picker(self):
        """Open color picker."""
        current = config.get('color', '#FF0000')
        color = QColorDialog.getColor(QColor(current), self, "Pick Color")
        if color.isValid():
            hex_color = color.name()
            config.set('color', hex_color)
            self._update_color_display()

    def _update_color_display(self):
        """Update color button display."""
        hex_color = config.get('color', '#FF0000')
        self.color_btn.setStyleSheet(f"background-color: {hex_color};")

    def update_status(self, status):
        """Update status label."""
        self.status_label.setText(f"Status: {status}")

    def closeEvent(self, event):
        """Handle window close."""
        config.set('highlight_pressed_key', self.highlight_pressed.isChecked())
        config.set('launch_at_startup', self.startup_checkbox.isChecked())
        event.accept()
