import curses
from .ui_element import UIElement, Checkbox, TextInput, PopupButton

class ToolbarManager:
    @staticmethod
    def draw_top_toolbar(win, file_menu_open, elements_menu_open, canvas_elements, macros_menu_open, edit_menu_open):
        # Top toolbar on row 0 using blue background.
        try:
            win.attron(curses.color_pair(2))
            win.addstr(0, 2, " File ")
            win.addstr(0, 10, " Edit ")
            win.addstr(0, 18, " Macros ")
            win.addstr(0, 28, " Elements ")
            win.addstr(0, 40, " Delete Control ")
            win.addstr(0, 58, " Help ")
            win.attroff(curses.color_pair(2))
        except curses.error:
            pass

        if file_menu_open:
            # Draw dropdown list for file menu above the toolbar and canvas.
            try:
                file_options = ["New", "Save", "Load", "Export", "Exit"]
                for idx, option in enumerate(file_options):
                    win.addstr(1 + idx, 2, option, curses.color_pair(2) | curses.A_BOLD)
            except curses.error:
                pass

        if edit_menu_open:
            # Draw dropdown list for edit menu.
            try:
                start_x = 10
                edit_options = ["Undo", "Redo", "Cut", "Paste"]
                for idx, option in enumerate(edit_options):
                    win.addstr(1 + idx, start_x, option, curses.color_pair(2))
            except curses.error:
                pass

        if macros_menu_open:
            # Draw dropdown list for macros menu.
            try:
                start_x = 18
                macros_options = ["Start/Stop", "Play Once", "Play Many", "Open Macro", "Save Macro"]
                for idx, option in enumerate(macros_options):
                    win.addstr(1 + idx, start_x, option, curses.color_pair(2))
            except curses.error:
                pass

        if elements_menu_open:
            # Draw dropdown list of current canvas elements below the "Elements" menu.
            try:
                start_x = 28
                for idx, el in enumerate(canvas_elements):
                    display_str = f"{idx}: {el.__class__.__name__} - {el.text}"
                    win.addstr(1 + idx, start_x, display_str, curses.color_pair(2))
            except curses.error:
                pass

    @staticmethod
    def draw_left_toolbar(win):
        # Left vertical toolbar on the left side; starting at row 2.
        toolbar_items = [
            UIElement(3, 2, 10, "[ Button ]"),
            Checkbox(7, 2, "Checkbox"),
            TextInput(11, 2, 15, "[ TextBox ]"),
            PopupButton(15, 2, 10, "[ Popup ]")
        ]
        try:
            win.addstr(2, 2, "Elements:", curses.A_BOLD | curses.color_pair(1))
            win.vline(2, 20, curses.ACS_VLINE, curses.LINES - 4)
        except curses.error:
            pass
        for item in toolbar_items:
            item.draw(win)
        return toolbar_items

    @staticmethod
    def draw_right_toolbar(win, selected_element, max_x):
        # Right properties panel on the right side.
        start_x = max_x - 25
        try:
            win.vline(1, start_x - 1, curses.ACS_VLINE, curses.LINES - 3)
            win.addstr(1, start_x, "Properties:", curses.A_BOLD | curses.color_pair(1))
        except curses.error:
            pass
        if selected_element:
            props = [
                f"Type: {selected_element.__class__.__name__}",
                f"X: {selected_element.x}",
                f"Y: {selected_element.y}",
                f"Width: {selected_element.width}",
                f"Text: {selected_element.text}"
            ]
            for i, prop in enumerate(props):
                try:
                    win.addstr(3 + i, start_x, prop, curses.color_pair(1))
                except curses.error:
                    pass
        else:
            try:
                win.addstr(3, start_x, "None", curses.color_pair(1))
            except curses.error:
                pass