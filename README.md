# Qurderer

**Qurderer** is a powerful Python framework for building modern PyQt5 applications with a focus on simplicity and maintainability. It provides a comprehensive set of decorators and utilities that streamline the development of complex desktop interfaces by abstracting away common patterns and boilerplate code.

The framework is designed to address the challenges of managing multiple windows, screens, and application state in PyQt5 applications. By leveraging decorators and a consistent architecture, Qurderer enables developers to create robust applications with less code and better organization.

---

## Key Features

- **Window Management**:
  - Create and manage multiple windows with the `@Window` decorator
  - Build main application windows with the `@MainWindow` decorator
  - Navigate between windows with history tracking
  - Customize window properties (size, position, resizability)

- **Screen Management**:
  - Create and navigate between multiple screens with the `@Screen` decorator
  - Automatic screen transitions with history tracking
  - Support for screen-specific layouts and widgets
  - Optional automatic UI reload when screens are displayed

- **Style Management**:
  - Apply styles to windows and widgets using the `@Style` decorator
  - Support for both file-based and string-based stylesheets
  - Theme color customization for consistent UI

- **Configuration Management**:
  - Inject global configurations with the `@useConfig` decorator
  - Access application settings from any component
  - Centralized configuration management

- **Session Storage**:
  - In-memory session storage with the `@useSessionStorage` decorator
  - Store and retrieve temporary data between screens
  - Persistent data management during application runtime

- **UI Components**:
  - **Notifications**: Customizable notification system with different types (success, error, info) and progress bars
  - **Floating Dialogs**: Modal dialog system with customizable backdrop, supporting both white and black themes
  - **Toggle Switch**: Animated toggle switch component with customizable appearance

---

## Installation

You can install **Qurderer** directly from the source code by cloning the repository:

```bash
git clone https://github.com/davidleonstr/Qurderer.git
cd Qurderer
pip install .
```
**Or for development:**
```bash
git clone https://github.com/davidleonstr/Qurderer.git
cd Qurderer
pip install -e .
```

---

## Example usage

### Main Window Setup

```python
import Qurderer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget
from typing import Callable

@Qurderer.MainWindow('Main Window', [100, 100, 600, 400], QIcon(), resizable=True, maximizable=True)
class MyApp(QMainWindow):
    # Type hints for better IDE support
    title: str
    windowGeometry: list
    icon: QIcon
    addScreen: Callable[[QWidget], None]
    setScreen: Callable[[str], None]
    createWindow: Callable[[QMainWindow], None]
    setWindow: Callable[[str], None]
    closeWindow: Callable[[str], None]
    onWindowClose: Callable[[], None]
    goBack: Callable[[], None]
    screens: dict
    windows: dict

    def __init__(self):
        """Initialize the main window and add screens."""
        super().__init__()

        # Add screen
        screen = ScreenClass(self)
        self.addScreen(screen)

        # Set the initial screen
        self.setScreen(screen.name)
```

### Screen Definition

```python
import Qurderer
from PyQt5.QtWidgets import QWidget
from typing import Callable

@Qurderer.Screen('screen', autoreloadUI=False) 
class ScreenClass(QWidget):
    # Type hints for better IDE support
    name: str
    screenName: str
    reloadUI: Callable[[], None]

    def __init__(self, parent):
        super().__init__(parent)
        self.widgetParent = parent  # Necessary if autoreloadUI = true
        self.UI(parent)

    def UI(self, parent) -> None:  # Necessary if autoreloadUI = true
        """
        The entire UI is loaded here.
        """
        pass
```

### Popup Window

```python
import Qurderer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from typing import List

@Qurderer.Window('popup', 'Popup Window', [710, 100, 400, 150], QIcon(), resizable=False)
class PopupWindow(QMainWindow):
    # Type hints for better IDE support
    name: str
    title: str
    windowGeometry: List[int]
    windowParent: object

    def __init__(self, parent):
        super().__init__(parent)
```

### Complete Application Example

```python
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
        self.createWindow(OtherPopupWindow(self))

@Qurderer.Screen('main')
@Qurderer.useConfig(config)
@Qurderer.useSessionStorage()
class MainScreen(QWidget):
    """Main screen with session storage and button interaction."""
    def __init__(self, parent):
        """Initialize the main screen's UI elements and session storage."""
        super().__init__(parent)
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent) -> None:
        layout = QVBoxLayout()

        # UI elements
        label = QLabel('Main Screen')
        label.setAlignment(Qt.AlignCenter)

        # Example of session storage
        self.sessionStorage.setItem('test<1>', 'hello world!')
        sessionLabel = QLabel(f"Session data: {self.sessionStorage.getItem('test<1>')}")
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

@Qurderer.Window('popup', 'Popup Window', [710, 100, 400, 150], QIcon(), resizable=False)
@Qurderer.useSessionStorage()
class PopupWindow(QMainWindow):
    """Popup window with screen management and session storage."""
    def __init__(self, parent):
        """Initialize the popup window with screen management."""
        super().__init__(parent)
        self.mainWindow = parent

        # Create and add the main popup screen
        self.mainScreen = PopupMainScreen(self)
        self.addScreen(self.mainScreen)
        self.setScreen(self.mainScreen.name)

    def closePopup(self):
        """Close the popup window."""
        self.mainWindow.closeWindow(self.name)

@Qurderer.Screen('popup-main')
@Qurderer.useSessionStorage()
class PopupMainScreen(QWidget):
    """Main screen for the popup window."""
    def __init__(self, parent):
        """Initialize the popup main screen."""
        super().__init__(parent)
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent) -> None:
        """Set up the user interface."""
        # Crear el layout principal
        mainLayout = QVBoxLayout()

        # UI elements
        label = QLabel('This is a popup window')
        label.setAlignment(Qt.AlignCenter)

        # Button to close the popup window
        buttonClose = QPushButton('Close Popup')
        buttonClose.clicked.connect(parent.closePopup)

        # Button to get session data
        buttonGetSession = QPushButton('Get Session Data')
        buttonGetSession.clicked.connect(self.showSessionData)

        # Example of ToggleSwitch
        toggle = Qurderer.components.ToggleSwitch(self, checked=True)

        # Add widgets to the layout
        mainLayout.addWidget(label)
        mainLayout.addWidget(buttonClose)
        mainLayout.addWidget(buttonGetSession)
        mainLayout.addWidget(toggle)

        # Set the layout
        self.setLayout(mainLayout)

    def showSessionData(self):
        """Show session data in a notification."""
        value = self.sessionStorage.getItem('test<1>')
        Qurderer.components.Notify(f'Session data: {value}', 3000, self.widgetParent)

@Qurderer.Window('otherpopup', 'Other Popup Window', [710, 285, 400, 150], QIcon(), resizable=False)
@Qurderer.useSessionStorage()
class OtherPopupWindow(QMainWindow):
    """Popup window with screen management."""
    def __init__(self, parent):
        """Initialize the popup window with screen management."""
        super().__init__(parent)
        self.mainWindow = parent

        # Add and set initial screen
        self.mainScreen = OtherNoneScreen(self)
        self.addScreen(self.mainScreen)
        self.setScreen(self.mainScreen.name)

    def closePopup(self):
        """Close the popup window."""
        self.mainWindow.closeWindow(self.name)

@Qurderer.Screen('other-none', autoreloadUI=True)
@Qurderer.useSessionStorage()
class OtherNoneScreen(QWidget):
    """Screen for the other popup window."""
    def __init__(self, parent):
        """Initialize the screen."""
        super().__init__(parent)
        self.widgetParent = parent
        self.UI(parent)

    def UI(self, parent) -> None:
        """Set up the user interface."""
        # Crear el layout principal
        mainLayout = QVBoxLayout()

        # UI elements
        label = QLabel('Other-none Screen')
        label.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.reloadUI)

        # Add widgets to the layout
        mainLayout.addWidget(label)
        mainLayout.addWidget(buttonReloadUI)

        # Set the layout
        self.setLayout(mainLayout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
```
