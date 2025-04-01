import json
import os
from .ui_element import UIElement, Checkbox, TextInput, PopupButton

class UIManager:
    LAYOUT_FILE = "layout.json"  # Define LAYOUT_FILE here

    @staticmethod
    def save_layout(elements):
        with open(UIManager.LAYOUT_FILE, "w") as f:
            json.dump([el.to_dict() for el in elements], f, indent=4)

    @staticmethod
    def load_layout():
        if os.path.exists(UIManager.LAYOUT_FILE):
            with open(UIManager.LAYOUT_FILE, "r") as f:
                data = json.load(f)
                elements = []
                for item in data:
                    if item["type"] == "Checkbox":
                        elements.append(Checkbox.from_dict(item))
                    elif item["type"] == "TextInput":
                        elements.append(TextInput.from_dict(item))
                    elif item["type"] == "PopupButton":
                        elements.append(PopupButton.from_dict(item))
                    else:
                        elements.append(UIElement.from_dict(item))
                return elements
        return []