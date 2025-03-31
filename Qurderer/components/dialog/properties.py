"""
This file contains the constants and properties for the Dialog object in this module.

Modifying any property in this file requires making the same changes in related files.
"""

# Location of the file with the styles for the Notify object
STYLEPATH = "Qurderer/components/dialog/Dialog.css"
"""Path to the file containing the styles for the Dialog object."""

# Object names for each style
STYLETCOLOR = {
    "black": {
        "floatingDialog": "black-floatingDialog",
    },
    "white": {
        "floatingDialog": "white-floatingDialog",
    },
}
"""
Dictionary defining object names for each style.

Available styles:
- **black** → Black floatingDialog background.
- **white** → White floatingDialog background.
"""