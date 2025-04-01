import curses

class UIElement:
    def __init__(self, y, x, width, text=""):
        self.y = y
        self.x = x
        self.width = width
        self.text = text
        self.selected = False
        self.dragging = False
        self.resizing = False

    def draw(self, win):
        # Draw an outline around the element to show its boundaries.
        try:
            # Top border
            win.addch(self.y, self.x, curses.ACS_ULCORNER)
            for i in range(1, self.width + 1):
                win.addch(self.y, self.x + i, curses.ACS_HLINE)
            win.addch(self.y, self.x + self.width + 1, curses.ACS_URCORNER)
            # Middle row with text
            win.addch(self.y + 1, self.x, curses.ACS_VLINE)
            style = curses.color_pair(3) if self.selected else curses.color_pair(1)
            display_text = self.text.ljust(self.width)
            win.addstr(self.y + 1, self.x + 1, display_text[:self.width], style)
            win.addch(self.y + 1, self.x + self.width + 1, curses.ACS_VLINE)
            # Bottom border
            win.addch(self.y + 2, self.x, curses.ACS_LLCORNER)
            for i in range(1, self.width + 1):
                win.addch(self.y + 2, self.x + i, curses.ACS_HLINE)
            win.addch(self.y + 2, self.x + self.width + 1, curses.ACS_LRCORNER)
        except curses.error:
            pass

    def is_within(self, my, mx):
        # Assume standard UIElement occupies one row.
        return self.y == my and self.x <= mx < self.x + self.width

    def is_on_resize_handle(self, my, mx):
        # For a button element (UIElement with "[ Button ]" text), allow resizing if clicked on the right 2 columns.
        if "[ Button ]" in self.text:
            if my == self.y and self.x + self.width - 2 <= mx <= self.x + self.width:
                return True
        return False

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "y": self.y,
            "x": self.x,
            "width": self.width,
            "text": self.text
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["y"], data["x"], data["width"], data["text"])

class Checkbox(UIElement):
    def __init__(self, y, x, label, checked=False):
        text = f"[X] {label}" if checked else f"[ ] {label}"
        super().__init__(y, x, width=len(text), text=text)
        self.checked = checked
        self.label = label

    def toggle(self):
        self.checked = not self.checked
        self.text = f"[X] {self.label}" if self.checked else f"[ ] {self.label}"

    def to_dict(self):
        data = super().to_dict()
        data["checked"] = self.checked
        return data

    @classmethod
    def from_dict(cls, data):
        label = data["text"][4:]  # remove the "[ ] " or "[X] "
        return cls(data["y"], data["x"], label, checked=data.get("checked", False))

class TextInput(UIElement):
    def __init__(self, y, x, width, text=""):
        # A textbox is drawn with an outline and occupies 3 rows.
        super().__init__(y, x, width, text=text)
        self.editing = False

    def draw(self, win):
        # Override to include the outline logic from the base class.
        super().draw(win)

    def is_within(self, my, mx):
        # Consider the interactive area to be the middle row.
        return (self.y+1 == my) and (self.x+1 <= mx < self.x+self.width+1)

    def is_on_resize_handle(self, my, mx):
        # For TextInput, if the click is on the middle row near the right border.
        if my == self.y+1 and self.x + self.width - 2 <= mx <= self.x + self.width + 1:
            return True
        return False

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["y"], data["x"], data["width"], text=data["text"])

class PopupButton(UIElement):
    def __init__(self, y, x, width, text="Popup"):
        super().__init__(y, x, width, text=text)

    def show_popup(self, stdscr):
        max_y, max_x = stdscr.getmaxyx()
        height, width = 5, 30
        begin_y = max_y // 2 - height // 2
        begin_x = max_x // 2 - width // 2
        popup = curses.newwin(height, width, begin_y, begin_x)
        popup.box()
        popup.addstr(2, 2, "This is a popup!", curses.A_BOLD)
        popup.refresh()
        popup.getch()  # Wait for any key press to dismiss
        del popup

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(data["y"], data["x"], data["width"], text=data["text"])