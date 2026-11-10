#!/usr/bin/env python3
"""Moborots Recovery OS - graphical entry point."""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from system_info import collect_system_info
from disk_manager import collect_disk_info
from backup import copy_path


class InfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        refresh = QPushButton("Refresh system information")
        refresh.clicked.connect(self.refresh)
        layout.addWidget(refresh)
        layout.addWidget(self.output)
        self.refresh()

    def refresh(self):
        self.output.setPlainText(collect_system_info())


class DiskTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        note = QLabel("Read-only overview. This page does not modify disks or partitions.")
        note.setWordWrap(True)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        refresh = QPushButton("Refresh disk information")
        refresh.clicked.connect(self.refresh)
        layout.addWidget(note)
        layout.addWidget(refresh)
        layout.addWidget(self.output)
        self.refresh()

    def refresh(self):
        self.output.setPlainText(collect_disk_info())


class BackupTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        note = QLabel("Copy files or folders to another location. The source is not modified.")
        note.setWordWrap(True)
        button = QPushButton("Choose source and backup destination")
        button.clicked.connect(self.run_backup)
        layout.addWidget(note)
        layout.addWidget(button)
        layout.addStretch(1)

    def run_backup(self):
        source = QFileDialog.getExistingDirectory(self, "Select source folder")
        if not source:
            return
        destination = QFileDialog.getExistingDirectory(self, "Select backup destination")
        if not destination:
            return
        try:
            result = copy_path(source, destination)
            QMessageBox.information(self, "Backup completed", result)
        except Exception as exc:
            QMessageBox.critical(self, "Backup failed", str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moborots Recovery OS")
        self.resize(980, 650)
        tabs = QTabWidget()
        tabs.addTab(InfoTab(), "System")
        tabs.addTab(DiskTab(), "Disks")
        tabs.addTab(BackupTab(), "Backup")
        self.setCentralWidget(tabs)
        self.statusBar().showMessage("Live recovery environment • Read-only diagnostics")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Moborots Recovery OS")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
