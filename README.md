# Qurderer

**Qurderer** is a Python package designed to simplify the management of windows, screens, styles, global configurations, and session storage in PyQt5 applications. It provides a set of decorators and utilities that make it easier to create and manage complex graphical interfaces.

---

## Key Features

- **Window and screen management**: Allows the creation and navigation between multiple screens and windows.
- **Custom styles**: Applies styles to windows and widgets using stylesheets (CSS) or directly from files.
- **Global configuration**: Injects global configurations into classes that require them.
- **Session storage**: Provides an in-memory session storage system for managing temporary data.
- **Notifications**: Includes a customizable notification system with different types (success, error, info) and progress bars.
- **Floating Dialogs**: Provides a modal dialog system with a customizable backdrop, supporting both white and black themes.
- **Automatic reload on screen display**: Provides an automatic UI recharge system.

---

## Installation

You can install **Qurderer** directly from the source code by cloning the repository:

```bash
git clone https://github.com/davidleonstr/Qurderer.git
cd Qurderer
pip install .
```

---

## Example usage

**MainWindow**
```python
import Qurderer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

@Qurderer.MainWindow('Main Window', [100, 100, 600, 400], QIcon())
class MyApp(QMainWindow):
    def __init__(self):
        """Initialize the main window and add screens."""
        super().__init__()

        # Add screen
        screen = ScreenClass(self)
        self.addScreen(screen)

        # Set the initial screen
        self.setScreen(screen.name)
```

**Screen**
```python
import Qurderer
from PyQt5.QtWidgets import QWidget

@Qurderer.Screen('screen', autoreloadUI=False) 
"""
AutoreloadUI = True if you need to reload the screen whenever it is displayed.
"""
class ScreenClass(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgetParent = parent # Necessary if autoreloadUI = true
        self.UI(parent)

    def UI(self, parent) -> None: # Necessary if autoreloadUI = true
        """
        The entire UI is loaded here.
        """
        pass
```

**Window**
```python
import Qurderer
from PyQt5.QtWidgets import QMainWindow

@Qurderer.Window('popup', 'Popup Window', [710, 100, 400, 150])
class PopupWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
```

**Example**
```python
"""
Main test application using Qurderer for PyQt5.

This script creates a basic application using PyQt5 with multiple screens, notifications, 
and session storage management. It uses the `Qurderer` package to manage windows, styles, 
session data, and notifications. The application demonstrates the creation of a main window 
and multiple screens (e.g., MainScreen, OtherScreen, PopupScreen) with functionality for 
setting and getting session data, managing window screens, and displaying notifications.

Modules:
    - sys: Provides access to system-specific parameters and functions.
    - PyQt5.QtWidgets: Contains widgets and classes to build the application's UI.
    - PyQt5.QtGui: Contains classes for GUI-related functionality like icons.
    - PyQt5.QtCore: Provides core non-GUI functionality, such as Qt constants.
    - dataclasses: Provides the `dataclass` decorator for creating simple classes for storing data.

Classes:
    Config:
        - A simple configuration class storing a message.
    MyApp:
        - The main window of the application, which manages the addition of screens, 
          window creation, and screen navigation.
    MainScreen:
        - Represents the main screen of the application, including buttons, labels, and 
          session storage functionality.
    OtherScreen:
        - Represents an alternative screen that displays session data and has navigation buttons.
    PopupWindow:
        - A small popup window with labels and buttons to interact with the session and 
          notifications.

Decorators:
    - @Qurderer.MainWindow: Adds title, size, and icon configuration to the main window.
    - @Qurderer.Style: Applies a specified style to the windows and widgets.
    - @Qurderer.useConfig: Injects configuration data into the screen's context.
    - @Qurderer.useSessionStorage: Manages session storage for each screen.
    - @Qurderer.Screen: Marks a class as a screen and associates it with a name.
    - @Qurderer.Window: Marks a class as a window, configuring its properties like name, 
      title, and size.
"""

import Qurderer
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from dataclasses import dataclass

# Example of useStyle
style = '''
QPushButton {
    background-color: #007BFF;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
    border: none;
}
QPushButton:hover {
    background-color: #0056b3; 
}
QPushButton:pressed {
    background-color: #004080;
}

QLabel {
    font-size: 16px;
    font-weight: semibold; 
}
'''

# Configuration example class
@dataclass
class Config:
    message = 'hello world!'

# Global config
config = Config()

@Qurderer.MainWindow('Main Window', [100, 100, 600, 400], QIcon())
@Qurderer.Style(style)
@Qurderer.useConfig(config)
@Qurderer.useSessionStorage()
class MyApp(QMainWindow):
    """Main window for the application that manages multiple screens and notifications."""
    def __init__(self):
        """Initialize the main window and add screens."""
        super().__init__()

        # Add screens
        mainScreen = MainScreen(self)
        otherScreen = OtherScreen(self)
        self.addScreen(mainScreen)
        self.addScreen(otherScreen)

        # Set the initial screen
        self.setScreen(mainScreen.name)

        # Create a popup window
        self.createWindow(PopupWindow(self))

@Qurderer.Screen('main')
@Qurderer.useConfig(config)
@Qurderer.useSessionStorage()
class MainScreen(QWidget):
    """Main screen with session storage and button interaction."""
    def __init__(self, parent):
        """Initialize the main screen's UI elements and session storage."""
        super().__init__(parent)
        self.UI(parent)

    def UI(self, parent) -> None:
        layout = QVBoxLayout()

        # UI elements
        label = QLabel('Main Screen')
        label.setAlignment(Qt.AlignCenter)

        # Example of session storage
        self.sessionStorage.setItem('test<1>', 'hello world!')
        sessionLabel = QLabel(f'Session data: {self.sessionStorage.getItem('test<1>')}')
        sessionLabel.setAlignment(Qt.AlignCenter)

        # Example of configuration
        configLabel = QLabel(f'Configuration data: {self.Config.message}')
        configLabel.setAlignment(Qt.AlignCenter)

        # Button to show a notification
        buttonNotify = QPushButton('Show Notification')
        buttonNotify.clicked.connect(lambda: Qurderer.components.Notify('This is a notification!', 3000, parent))

        # Button to navigate to another screen
        buttonNavigate = QPushButton('Go to Other Screen')
        buttonNavigate.clicked.connect(lambda: parent.setScreen('other'))

        # Button to open a popup window
        buttonPopup = QPushButton('Open Popup')
        buttonPopup.clicked.connect(lambda: parent.createWindow(PopupWindow(parent)))

        buttonClosePopup = QPushButton('Close Popup')
        buttonClosePopup.clicked.connect(lambda: parent.closeWindow(PopupWindow(parent).name))

        # Dialog example
        dialogLayout = QVBoxLayout()
        dialogLayout.addWidget(QLabel('Hello in dialog.'))

        dialog = Qurderer.components.Dialog(parent, dialogLayout)

        buttonDialog = QPushButton('Close Dialog')
        buttonDialog.clicked.connect(dialog.close)

        dialog.addWidget(buttonDialog)

        buttonOpenDialog = QPushButton('Open Dialog')
        buttonOpenDialog.clicked.connect(dialog.show)

        buttonSetSessionData = QPushButton('Set test<2>')
        buttonSetSessionData.clicked.connect(lambda: self.sessionStorage.setItem('test<2>', 'hello world!'))
        
        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(configLabel)
        layout.addWidget(sessionLabel)
        layout.addWidget(buttonNotify)
        layout.addWidget(buttonNavigate)
        layout.addWidget(buttonPopup)
        layout.addWidget(buttonClosePopup)
        layout.addWidget(buttonOpenDialog)
        layout.addWidget(buttonSetSessionData)

        # Set the layout
        self.setLayout(layout)

@Qurderer.Screen('other', autoreloadUI=True)
@Qurderer.useSessionStorage()
class OtherScreen(QWidget):
    """Secondary screen with session storage and navigation."""
    def __init__(self, parent):
        """Initialize the other screen's UI elements and session storage."""
        super().__init__(parent)
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent) -> None:
        layout = QVBoxLayout()

        # UI elements
        label = QLabel('Other Screen')
        label.setAlignment(Qt.AlignCenter)

        # Example of session storage
        sessionLabel = QLabel(f"Session data test<1>: {self.sessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        sessionTestReload = QLabel(f"Session data test<2>: {self.sessionStorage.getItem('test<2>')}")
        sessionTestReload.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.reloadUI)

        # Button to navigate back to the main screen
        buttonBack = QPushButton('Go Back to Main Screen')
        buttonBack.clicked.connect(lambda: parent.setScreen('main'))

        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(sessionLabel)
        layout.addWidget(sessionTestReload)
        layout.addWidget(buttonBack)
        layout.addWidget(buttonReloadUI)

        # Set the layout
        self.setLayout(layout)

@Qurderer.Window('popup', 'Popup Window', [710, 100, 400, 150])
@Qurderer.useSessionStorage()
class PopupWindow(QMainWindow):
    """Popup window with buttons and session management."""
    def __init__(self, parent):
        """Initialize the popup window's UI elements."""
        super().__init__(parent)
        self.parent = parent

        # Main layout
        layout = QVBoxLayout()

        # UI elements
        label = QLabel('This is a popup window')
        label.setAlignment(Qt.AlignCenter)

        # Button to close the popup window
        buttonClose = QPushButton('Close Popup')
        buttonClose.clicked.connect(self.closePopup)

        # Button to get session data
        buttonGetSession = QPushButton('Get Session Data')
        buttonGetSession.clicked.connect(self.showSessionData)

        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(buttonClose)
        layout.addWidget(buttonGetSession)

        # Set the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def closePopup(self):
        """Close the popup window."""
        self.parent.closeWindow(self.name)

    def showSessionData(self):
        """Show session data in a notification."""
        value = self.sessionStorage.getItem('test<1>')
        Qurderer.components.Notify(f'Session data: {value}', 3000, self)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
```