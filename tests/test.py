import Qurderer
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from dataclasses import dataclass
from Qurderer.stores import useState, Subscribeable

# Example of Style
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

QSpinBox, QLineEdit {
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 14px;
}
'''

# Configuration example class
@dataclass
class Config:
    message = 'hello world!'

# Global config
config = Config()

# Example of Subscribeable
counter = Subscribeable(0)

@Qurderer.MainWindow('Main Window', [100, 100, 600, 400], QIcon())
@Qurderer.Style(style)
@Qurderer.UseConfig(config)
@Qurderer.UseSessionStorage()
class MyApp(QMainWindow):
    """Main window for the application that manages multiple screens and notifications."""
    def __init__(self):
        """Initialize the main window and add screens."""
        super().__init__()

        # Add screens
        mainScreen = MainScreen(self)
        otherScreen = OtherScreen(self)
        storeScreen = StoreScreen(self)
        self.addScreen(mainScreen)
        self.addScreen(otherScreen)
        self.addScreen(storeScreen)

        # Set the initial screen
        self.setScreen(mainScreen.name)

        # Create a popup window
        self.createWindow(PopupWindow(self))
        self.createWindow(OtherPopupWindow(self))

@Qurderer.Screen('main')
@Qurderer.UseConfig(config)
@Qurderer.UseSessionStorage()
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
        self.SessionStorage.setItem('test<1>', 'hello world!')
        sessionLabel = QLabel(f"Session data: {self.SessionStorage.getItem('test<1>')}")
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
        
        # Button to navigate to store screen
        buttonStore = QPushButton('Go to Store Screen')
        buttonStore.clicked.connect(lambda: parent.setScreen('store'))

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
        buttonSetSessionData.clicked.connect(lambda: self.SessionStorage.setItem('test<2>', 'hello world!'))
        
        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(configLabel)
        layout.addWidget(sessionLabel)
        layout.addWidget(buttonNotify)
        layout.addWidget(buttonNavigate)
        layout.addWidget(buttonStore)
        layout.addWidget(buttonPopup)
        layout.addWidget(buttonClosePopup)
        layout.addWidget(buttonOpenDialog)
        layout.addWidget(buttonSetSessionData)

        # Set the layout
        self.setLayout(layout)

@Qurderer.Screen('other', autoreloadUI=True)
@Qurderer.UseSessionStorage()
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
        sessionLabel = QLabel(f"Session data test<1>: {self.SessionStorage.getItem('test<1>')}")
        sessionLabel.setAlignment(Qt.AlignCenter)

        sessionTestReload = QLabel(f"Session data test<2>: {self.SessionStorage.getItem('test<2>')}")
        sessionTestReload.setAlignment(Qt.AlignCenter)

        buttonReloadUI = QPushButton('Reload UI')
        buttonReloadUI.clicked.connect(self.reloadUI)

        # Button to navigate back to the main screen
        buttonBack = QPushButton('Go Back to Main Screen')
        buttonBack.clicked.connect(lambda: parent.setScreen('main'))
        
        # Button to navigate to store screen
        buttonStore = QPushButton('Go to Store Screen')
        buttonStore.clicked.connect(lambda: parent.setScreen('store'))

        # Add widgets to the layout
        layout.addWidget(label)
        layout.addWidget(sessionLabel)
        layout.addWidget(sessionTestReload)
        layout.addWidget(buttonBack)
        layout.addWidget(buttonStore)
        layout.addWidget(buttonReloadUI)

        # Set the layout
        self.setLayout(layout)

@Qurderer.Screen('store')
class StoreScreen(QWidget):
    """Screen demonstrating the use of useState and Subscribeable."""
    def __init__(self, parent):
        """Initialize the store screen with useState and Subscribeable examples."""
        super().__init__(parent)
        self.widgetParent = parent
        
        # Create useState examples
        self.count, self.setCount, self.subscribeCount = useState(0)
        self.text, self.setText, self.subscribeText = useState("Hello from useState!")
        
        # Subscribe to counter changes
        counter.subscribe(self.onCounterChange)
        
        # Create UI
        self.UI(parent)
        
        # Subscribe to state changes
        self.subscribeCount(self.onCountChange)
        self.subscribeText(self.onTextChange)
        
        # Update UI with initial values
        self.countLabel.setText(f"Count: {self.count()}")
        self.textLabel.setText(f"Text: {self.text()}")
        self.counterLabel.setText(f"Counter: {counter.value}")

    def UI(self, parent) -> None:
        """Set up the user interface for the store screen."""
        mainLayout = QVBoxLayout()
        
        # Title
        title = QLabel('Store Examples')
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)
        
        # useState example section
        useStateSection = QVBoxLayout()
        useStateTitle = QLabel('useState Example')
        useStateTitle.setAlignment(Qt.AlignCenter)
        useStateSection.addWidget(useStateTitle)
        
        # Count example
        countLayout = QHBoxLayout()
        self.countLabel = QLabel(f"Count: {self.count()}")
        countButton = QPushButton("Increment Count")
        countButton.clicked.connect(self.incrementCount)
        countLayout.addWidget(self.countLabel)
        countLayout.addWidget(countButton)
        useStateSection.addLayout(countLayout)
        
        # Text example
        textLayout = QHBoxLayout()
        self.textLabel = QLabel(f"Text: {self.text()}")
        textInput = QLineEdit(self.text())
        textInput.textChanged.connect(self.setText)
        textLayout.addWidget(self.textLabel)
        textLayout.addWidget(textInput)
        useStateSection.addLayout(textLayout)
        
        mainLayout.addLayout(useStateSection)
        
        # Subscribeable example section
        subscribeableSection = QVBoxLayout()
        subscribeableTitle = QLabel('Subscribeable Example')
        subscribeableTitle.setAlignment(Qt.AlignCenter)
        subscribeableSection.addWidget(subscribeableTitle)
        
        # Counter example
        counterLayout = QHBoxLayout()
        self.counterLabel = QLabel(f"Counter: {counter.value}")
        counterButton = QPushButton("Increment Counter")
        counterButton.clicked.connect(self.incrementCounter)
        counterLayout.addWidget(self.counterLabel)
        counterLayout.addWidget(counterButton)
        subscribeableSection.addLayout(counterLayout)
        
        mainLayout.addLayout(subscribeableSection)
        
        # Navigation buttons
        navLayout = QHBoxLayout()
        buttonBack = QPushButton('Go Back to Main Screen')
        buttonBack.clicked.connect(lambda: parent.setScreen('main'))
        buttonOther = QPushButton('Go to Other Screen')
        buttonOther.clicked.connect(lambda: parent.setScreen('other'))
        navLayout.addWidget(buttonBack)
        navLayout.addWidget(buttonOther)
        mainLayout.addLayout(navLayout)
        
        # Set the layout
        self.setLayout(mainLayout)
    
    def incrementCount(self):
        """Increment the count state."""
        self.setCount(self.count() + 1)
    
    def incrementCounter(self):
        """Increment the counter Subscribeable."""
        counter.value = counter.value + 1
    
    def onCountChange(self, newValue):
        """Handle count state changes."""
        self.countLabel.setText(f"Count: {newValue}")
        Qurderer.components.Notify(f"Count changed to {newValue}", 1000, self.widgetParent)
    
    def onTextChange(self, newValue):
        """Handle text state changes."""
        self.textLabel.setText(f"Text: {newValue}")
    
    def onCounterChange(self, newValue):
        """Handle counter Subscribeable changes."""
        self.counterLabel.setText(f"Counter: {newValue}")
        Qurderer.components.Notify(f"Counter changed to {newValue}", 1000, self.widgetParent)

@Qurderer.Window('popup', 'Popup Window', [710, 100, 400, 150], QIcon(), resizable=False)
@Qurderer.UseSessionStorage()
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
@Qurderer.UseSessionStorage()
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
        value = self.SessionStorage.getItem('test<1>')
        Qurderer.components.Notify(f'Session data: {value}', 3000, self.widgetParent)

@Qurderer.Window('otherpopup', 'Other Popup Window', [710, 285, 400, 150], QIcon(), resizable=False)
@Qurderer.UseSessionStorage()
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
@Qurderer.UseSessionStorage()
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