"""
This module defines the Notify class, which represents an on-screen notification in a PyQt5 application.

The class handles displaying messages with custom icons, progress bars, and predefined styles.
A decorator is used to apply styles from an external file.
"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QProgressBar, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

# Decorator for applying styles to PyQt5 widgets
from ...modules.Style import *

# Class for creating Pixmap icons
from ...modules.Icon import *

# Importing style properties and configuration
from .properties import STYLEBAR, STYLEPATH, STYLETCOLOR, ICONS


@Style(STYLEPATH, True)
class Notify(QWidget):
    """
    Represents an on-screen notification within a parent window.

    This class allows displaying messages with different notification types 
    (success, error, info) and customizable styles. It also includes a progress bar 
    indicating the notification duration.
    """

    cont = {}
    """Dictionary tracking the number of notifications per parent window."""

    def __init__(
            self, 
            message: str, 
            duration: int = 3000, 
            parent=None, 
            type: str = 'success', 
            color: str = 'black', 
            customIcon: QPixmap = None,
            notificationsLimit: int = 7,
            characterLimit: int = 60
        ):
        """
        Initializes a Notify object.

        Args:
            message (str): The notification message.
            duration (int, optional): Duration before the notification disappears (in milliseconds). Default is 3000ms.
            parent (QWidget, optional): The parent widget where the notification will be displayed.
            type (str, optional): The type of notification ('success', 'error', 'info'). Default is 'success'.
            color (str, optional): The theme color ('black' or 'white'). Default is 'black'.
            customIcon (QPixmap, optional): A custom icon to use instead of the default.
            notificationsLimit (int, optional): Parent notification limiter. Default is 7.
            characterLimit (int, optional): Character limit in the notification. Default is 60.
        """
        super().__init__(parent)
        self.parent = parent
        self.duration = duration
        self.elapsedTime = 0
        self.message = message

        if len(message) > characterLimit:
            self.message = message[:characterLimit - 1] + '...'

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QFrame(self)
        self.container.setMinimumWidth(270)

        if color in STYLETCOLOR:
            self.containerStyle = STYLETCOLOR[color]['QFrame']

        self.container.setObjectName(self.containerStyle)

        self.iconLabel = QLabel(self.container)

        if type in ICONS:
            self.icon = ICONS[type]()

        if customIcon is not None:
            self.icon = customIcon

        self.iconLabel.setPixmap(self.icon)

        self.messageLabel = QLabel(self.message, self.container)
        self.messageLabel.setObjectName(STYLETCOLOR[color]['QLabel'])

        self.progressBar = QProgressBar(self.container)

        if type in STYLEBAR:
            self.progressBarStyle = STYLEBAR[type]

        self.progressBar.setObjectName(self.progressBarStyle)

        self.progressBar.setFixedHeight(10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMaximum(self.duration)
        self.progressBar.setValue(0)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(8)
        self.contentLayout.addWidget(self.iconLabel, 0, Qt.AlignVCenter)  
        self.contentLayout.addWidget(self.messageLabel, 1, Qt.AlignVCenter)

        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.addLayout(self.contentLayout)
        self.containerLayout.addWidget(self.progressBar)
        self.containerLayout.setContentsMargins(20, 10, 20, 10)

        self.container.setLayout(self.containerLayout)
        self.container.adjustSize()

        if self.parent in Notify.cont:
            Notify.cont[self.parent] += 1
        else:
            Notify.cont[self.parent] = 1

        self.notificationCount = Notify.cont[self.parent]

        if self.notificationCount > notificationsLimit:
            return

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.container)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)
        self.adjustSize()

        self.updatePosition()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(30)

        QTimer.singleShot(duration, self.close)

        self.show()

    def updatePosition(self) -> None:
        """Updates the notification's position relative to its parent window."""
        if self.parent:
            x = self.parent.x() + self.parent.width() - self.width() - 20
            y = self.parent.y() + 40 + (self.notificationCount - 1) * 80
            self.move(x, y)

    def updateProgress(self) -> None:
        """Updates the progress bar and closes the notification when the duration ends."""
        self.elapsedTime += 30  
        self.progressBar.setValue(self.elapsedTime)

        if self.elapsedTime >= self.duration:
            self.timer.stop()
            self.close()

    def close(self) -> None:
        """Closes the notification and updates the notification count."""
        if self.parent in Notify.cont and Notify.cont[self.parent] > 0:
            Notify.cont[self.parent] -= 1
        super().close()
