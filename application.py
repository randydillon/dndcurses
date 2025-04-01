import curses
from .ui_manager import UIManager
from .toolbar_manager import ToolbarManager
from .popup_manager import PopupManager
from .ui_element import PopupButton, Checkbox, TextInput, UIElement  # Import Checkbox and other UI elements

class Application:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.elements = UIManager.load_layout()
        self.selected_element = None
        self.file_menu_open = False
        self.elements_menu_open = False
        self.macros_menu_open = False
        self.edit_menu_open = False
        self.log_message = ""
        self.crosshair_x, self.crosshair_y = -1, -1

    def initialize_curses(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
        self.stdscr.bkgd(' ', curses.color_pair(1))
        curses.curs_set(0)
        self.stdscr.nodelay(0)
        self.stdscr.keypad(1)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    def draw_ui(self):
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.clear()
        ToolbarManager.draw_top_toolbar(
            self.stdscr, self.file_menu_open, self.elements_menu_open, self.elements, self.macros_menu_open, self.edit_menu_open
        )
        left_toolbar = ToolbarManager.draw_left_toolbar(self.stdscr)
        ToolbarManager.draw_right_toolbar(self.stdscr, self.selected_element, max_x)
        for element in self.elements:
            element.draw(self.stdscr)
        if 0 <= self.crosshair_y < max_y and 0 <= self.crosshair_x < max_x:
            try:
                self.stdscr.addch(self.crosshair_y, self.crosshair_x, ord('+'), curses.color_pair(3))
            except curses.error:
                pass
        try:
            self.stdscr.addstr(max_y - 1, 0, "Log: " + self.log_message[:max_x - 5], curses.color_pair(1))
        except curses.error:
            pass
        self.stdscr.refresh()
        return left_toolbar

    def handle_keypress(self, key):
        self.log_message = f"Key pressed: {key} (Code: {key})"
        if key == 17:  # Option-Q
            self.log_message += " - Option-Q: Quit"
            return False  # Exit the application
        elif key == 19:  # Option-S
            UIManager.save_layout(self.elements)
            self.log_message += " - Option-S: Layout saved"
        elif key == 8:  # Option-H
            PopupManager.show_help_popup(self.stdscr)
            self.log_message += " - Option-H: Help popup shown"
        elif key == ord('e') and self.selected_element:
            PopupManager.edit_properties(self.stdscr, self.selected_element)
            self.log_message += " - 'e': Edit properties"
        elif key == 3:  # Option-C
            self.log_message += " - Option-C: No action performed"
        return True

    def handle_mouse_event(self, bstate, mx, my, left_toolbar):
        self.crosshair_x, self.crosshair_y = mx, my
        self.log_message = f"Mouse at ({mx},{my})"

        # Top toolbar clicks.
        if my == 0 and (bstate & curses.BUTTON1_PRESSED):
            if 2 <= mx <= 2 + len(" File "):
                self.file_menu_open = not self.file_menu_open
                self.edit_menu_open = False
                self.macros_menu_open = False
                self.elements_menu_open = False
                self.log_message += " - Toggled File menu"
                return
            elif 10 <= mx <= 10 + len(" Edit "):
                self.edit_menu_open = not self.edit_menu_open
                self.file_menu_open = False
                self.macros_menu_open = False
                self.elements_menu_open = False
                self.log_message += " - Toggled Edit menu"
                return
            elif 18 <= mx <= 18 + len(" Macros "):
                self.macros_menu_open = not self.macros_menu_open
                self.file_menu_open = False
                self.edit_menu_open = False
                self.elements_menu_open = False
                self.log_message += " - Toggled Macros menu"
                return
            elif 28 <= mx <= 28 + len(" Elements "):
                self.elements_menu_open = not self.elements_menu_open
                self.file_menu_open = False
                self.edit_menu_open = False
                self.macros_menu_open = False
                self.log_message += " - Toggled Elements menu"
                return
            elif 40 <= mx <= 40 + len(" Delete Control "):
                if self.selected_element in self.elements:
                    self.elements.remove(self.selected_element)
                    self.log_message += " - Deleted selected control"
                    self.selected_element = None
                return
            elif 58 <= mx <= 58 + len(" Help "):
                PopupManager.show_help_popup(self.stdscr)
                self.log_message += " - Help popup shown"
                return

        # File menu dropdown.
        if self.file_menu_open and my == 1 and 2 <= mx <= 20 and (bstate & curses.BUTTON1_PRESSED):
            UIManager.save_layout(self.elements)
            self.log_message += " - Saved via File menu"
            self.file_menu_open = False
            return

        # Elements menu dropdown.
        if self.elements_menu_open and my >= 1:
            start_x = 28
            idx = my - 1  # first item at row 1
            if 0 <= idx < len(self.elements):
                self.selected_element = self.elements[idx]
                self.log_message += f" - Selected element {idx} from Elements menu"
                self.elements_menu_open = False
                return

        # Macros menu dropdown.
        if self.macros_menu_open and my >= 1:
            start_x = 18
            macros_options = ["Start/Stop", "Play Once", "Play Many", "Open Macro", "Save Macro"]
            idx = my - 1  # first item at row 1
            if 0 <= idx < len(macros_options):
                self.log_message += f" - Selected '{macros_options[idx]}' from Macros menu"
                self.macros_menu_open = False
                # Add logic for handling each macro option here.
                return

        # Edit menu dropdown.
        if self.edit_menu_open and my >= 1:
            start_x = 10
            edit_options = ["Undo", "Redo", "Cut", "Paste"]
            idx = my - 1  # first item at row 1
            if 0 <= idx < len(edit_options):
                self.log_message += f" - Selected '{edit_options[idx]}' from Edit menu"
                self.edit_menu_open = False
                # Add logic for handling each edit option here.
                return

        # Left toolbar region: Drag elements onto the canvas with left-click.
        if bstate & curses.BUTTON1_PRESSED:
            for item in left_toolbar:
                # Allow clicking anywhere within the element's outline
                if item.y <= my <= item.y + 2 and item.x <= mx <= item.x + item.width + 1:
                    if isinstance(item, PopupButton):
                        new_element = PopupButton(my, mx + 25, 10, "[ Popup ]")
                    elif isinstance(item, Checkbox):
                        new_element = Checkbox(my, mx + 25, "New Checkbox")
                    elif isinstance(item, TextInput):
                        new_element = TextInput(my, mx + 25, 15, "")
                    elif isinstance(item, UIElement) and "[ Button ]" in item.text:
                        new_element = UIElement(my, mx + 25, 10, "[ Button ]")
                    else:
                        continue
                    # Adjust the initial position to center canvas
                    new_element.x = 30  # Example center canvas X position
                    new_element.y = 10  # Example center canvas Y position
                    self.elements.append(new_element)
                    self.selected_element = new_element
                    self.selected_element.dragging = True
                    self.log_message += " - Dragging new element from toolbar with left-click"
                    return

        # Handle dragging/resizing while the mouse is moved with BUTTON1_PRESSED.
        if bstate & curses.BUTTON1_PRESSED:
            if self.selected_element:
                if self.selected_element.dragging:
                    self.selected_element.x = mx
                    self.selected_element.y = my
                    self.log_message += f" - Dragging to ({mx},{my})"
                elif self.selected_element.resizing:
                    new_width = max(5, mx - self.selected_element.x - 1)
                    self.selected_element.width = new_width
                    self.log_message += f" - Resizing to width {new_width}"

        elif bstate & curses.BUTTON1_RELEASED:
            if self.selected_element:
                self.selected_element.dragging = False
                self.selected_element.resizing = False
                self.log_message += " - Dragging or resizing completed"

        # Right-click: select element for properties or movement.
        if bstate & curses.BUTTON3_PRESSED:
            for element in self.elements:
                if element.is_within(my, mx):
                    self.selected_element = element
                    self.log_message += " - Element selected via right-click"
                elif element.is_on_resize_handle(my, mx):
                    self.selected_element = element
                    self.selected_element.resizing = True
                    self.log_message += " - Resizing initiated via right-click"

        elif bstate & curses.BUTTON3_RELEASED:
            if self.selected_element:
                if self.selected_element.resizing:
                    self.selected_element.resizing = False
                    self.log_message += " - Resizing completed"
                elif isinstance(self.selected_element, PopupButton):
                    self.selected_element.show_popup(self.stdscr)
                    self.log_message += " - Popup displayed"
                else:
                    self.selected_element.x = mx
                    self.selected_element.y = my
                    self.log_message += f" - Moved to ({mx},{my})"

    def run(self):
        self.initialize_curses()
        while True:
            left_toolbar = self.draw_ui()
            key = self.stdscr.getch()
            if not self.handle_keypress(key):
                break
            if key == curses.KEY_MOUSE:
                try:
                    _id, mx, my, _z, bstate = curses.getmouse()
                except curses.error:
                    continue
                self.handle_mouse_event(bstate, mx, my, left_toolbar)