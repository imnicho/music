from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QComboBox, QGroupBox, QApplication, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QIcon
import sys
from version import __version__

class OctaveLightsWindow(QMainWindow):
    color_changed = Signal(str)
    highlight_changed = Signal(bool, str)
    enabled_changed = Signal(bool)
    startup_changed = Signal(bool)

    def __init__(self, config, midi_listener, octave_engine):
        super().__init__()
        self.config = config
        self.midi_listener = midi_listener
        self.octave_engine = octave_engine

        self.setWindowTitle("OctaveLights")
        self.setGeometry(100, 100, 500, 600)
        self.setWindowIcon(QIcon("assets/app.ico"))

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # ===== Enable/Disable Toggle =====
        toggle_layout = QHBoxLayout()
        toggle_label = QLabel("OctaveLights")
        toggle_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.toggle_btn = QPushButton("Enable")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(self.config.get("enabled", True))
        self.toggle_btn.setMinimumWidth(100)
        self.toggle_btn.toggled.connect(self._on_toggle)
        toggle_layout.addWidget(toggle_label)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        layout.addLayout(toggle_layout)

        # ===== Status Indicator =====
        status_layout = QHBoxLayout()
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: red; font-size: 20px;")
        self.status_text = QLabel("Keyboard not found")
        self.retry_btn = QPushButton("Retry")
        self.retry_btn.setMaximumWidth(80)
        self.retry_btn.clicked.connect(self._on_retry)
        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        status_layout.addWidget(self.retry_btn)
        layout.addLayout(status_layout)

        # ===== Settings Group =====
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()

        # Color picker
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Lighting Color:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            "white", "red", "orange", "yellow", "green", "cyan", "blue", "magenta"
        ])
        self.color_combo.setCurrentText(self.config.get("color", "white"))
        self.color_combo.currentTextChanged.connect(self._on_color_changed)
        color_layout.addWidget(self.color_combo)
        color_layout.addStretch()
        settings_layout.addLayout(color_layout)

        # Highlight pressed key
        highlight_layout = QHBoxLayout()
        self.highlight_check = QCheckBox("Highlight pressed key differently")
        self.highlight_check.setChecked(self.config.get("highlight_pressed", False))
        self.highlight_check.stateChanged.connect(self._on_highlight_changed)
        highlight_layout.addWidget(self.highlight_check)
        highlight_layout.addStretch()
        settings_layout.addLayout(highlight_layout)

        # Highlight color
        highlight_color_layout = QHBoxLayout()
        highlight_color_layout.addWidget(QLabel("  Highlight Color:"))
        self.highlight_color_combo = QComboBox()
        self.highlight_color_combo.addItems([
            "white", "red", "orange", "yellow", "green", "cyan", "blue", "magenta"
        ])
        self.highlight_color_combo.setCurrentText(self.config.get("highlight_color", "cyan"))
        self.highlight_color_combo.currentTextChanged.connect(self._on_highlight_color_changed)
        highlight_color_layout.addWidget(self.highlight_color_combo)
        highlight_color_layout.addStretch()
        settings_layout.addLayout(highlight_color_layout)

        # Launch at startup
        self.startup_check = QCheckBox("Launch at Windows startup")
        self.startup_check.setChecked(self.config.get("launch_at_startup", False))
        self.startup_check.stateChanged.connect(self._on_startup_changed)
        settings_layout.addWidget(self.startup_check)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # ===== About Section =====
        about_group = QGroupBox("About")
        about_layout = QVBoxLayout()

        version_label = QLabel(f"OctaveLights v{__version__}")
        version_label.setStyleSheet("font-weight: bold;")
        about_layout.addWidget(version_label)

        repo_label = QLabel('<a href="https://github.com/imnicho/music">GitHub Repository</a>')
        repo_label.setOpenExternalLinks(True)
        about_layout.addWidget(repo_label)

        warning_label = QLabel(
            "⚠️ Important: Close Native Instruments Komplete Kontrol software before using this app."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #ff6600; font-weight: bold;")
        about_layout.addWidget(warning_label)

        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        layout.addStretch()
        main_widget.setLayout(layout)

        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(1000)  # Update every 1s

        self._update_status()

    def _update_status(self):
        if self.midi_listener.is_connected():
            self.status_dot.setStyleSheet("color: green; font-size: 20px;")
            self.status_text.setText("Connected")
        else:
            self.status_dot.setStyleSheet("color: red; font-size: 20px;")
            self.status_text.setText("Keyboard not found")

    def _on_toggle(self, checked):
        self.toggle_btn.setText("Disable" if checked else "Enable")
        self.config.set("enabled", checked)
        self.enabled_changed.emit(checked)

    def _on_retry(self):
        if self.midi_listener.open_port():
            self._update_status()
        else:
            QMessageBox.warning(
                self,
                "Connection Failed",
                "Could not find Komplete Kontrol keyboard.\n\n"
                "Make sure:\n"
                "- Keyboard is connected via USB\n"
                "- Keyboard is powered on\n"
                "- Native Instruments drivers are installed"
            )

    def _on_color_changed(self, color_name):
        self.config.set("color", color_name)
        self.octave_engine.set_color(color_name)
        self.color_changed.emit(color_name)

    def _on_highlight_changed(self, state):
        enabled = state == Qt.CheckState.Checked
        self.config.set("highlight_pressed", enabled)
        color = self.highlight_color_combo.currentText()
        self.octave_engine.set_highlight_pressed(enabled, color)
        self.highlight_changed.emit(enabled, color)

    def _on_highlight_color_changed(self, color_name):
        self.config.set("highlight_color", color_name)
        if self.highlight_check.isChecked():
            self.octave_engine.set_highlight_pressed(True, color_name)
        self.highlight_changed.emit(self.highlight_check.isChecked(), color_name)

    def _on_startup_changed(self, state):
        enabled = state == Qt.CheckState.Checked
        self.config.set("launch_at_startup", enabled)
        if enabled:
            self._write_startup_registry()
        else:
            self._remove_startup_registry()
        self.startup_changed.emit(enabled)

    def _write_startup_registry(self):
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            exe_path = sys.executable
            winreg.SetValueEx(key, "OctaveLights", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except:
            pass

    def _remove_startup_registry(self):
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, "OctaveLights")
            winreg.CloseKey(key)
        except:
            pass

    def closeEvent(self, event):
        self.status_timer.stop()
        event.accept()
