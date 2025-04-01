import curses

class PopupManager:
    @staticmethod
    def edit_properties(stdscr, selected_element):
        if not selected_element:
            return
        curses.echo()
        max_y, max_x = stdscr.getmaxyx()
        height, width = 10, 40
        begin_y = max_y // 2 - height // 2
        begin_x = max_x // 2 - width // 2
        win = curses.newwin(height, width, begin_y, begin_x)
        win.box()
        win.addstr(1, 2, "Edit Properties", curses.A_BOLD)
        # Prompt for new text.
        prompt = f"Text [{selected_element.text}]: "
        win.addstr(3, 2, prompt)
        win.refresh()
        new_text = win.getstr(3, 2 + len(prompt)).decode("utf-8")
        if new_text.strip():
            selected_element.text = new_text

        # Prompt for new width.
        prompt = f"Width [{selected_element.width}]: "
        win.addstr(4, 2, prompt)
        win.refresh()
        new_width_str = win.getstr(4, 2 + len(prompt)).decode("utf-8")
        if new_width_str.strip():
            try:
                selected_element.width = max(5, int(new_width_str))
            except:
                pass

        # Prompt for new X.
        prompt = f"X [{selected_element.x}]: "
        win.addstr(5, 2, prompt)
        win.refresh()
        new_x_str = win.getstr(5, 2 + len(prompt)).decode("utf-8")
        if new_x_str.strip():
            try:
                selected_element.x = int(new_x_str)
            except:
                pass

        # Prompt for new Y.
        prompt = f"Y [{selected_element.y}]: "
        win.addstr(6, 2, prompt)
        win.refresh()
        new_y_str = win.getstr(6, 2 + len(prompt)).decode("utf-8")
        if new_y_str.strip():
            try:
                selected_element.y = int(new_y_str)
            except:
                pass

        curses.noecho()
        win.getch()  # Wait for one final key
        del win

    @staticmethod
    def show_help_popup(stdscr):
        # Centered help popup listing hotkeys.
        help_lines = [
            "Hotkeys:",
            "Option-Q: Quit",
            "Option-S: Save",
            "Option-H: Show Help",
            "e: Edit Properties (of selected control)",
            "Mouse Left-Click: Select/Drag/Resize",
            "Mouse Right-Click: Select for Properties",
            "File Menu: Click 'File' then 'Save'",
            "Delete Control: Click to delete selected control",
            "Elements Menu: Lists current elements",
            "",
            "Click or press any key to close..."
        ]
        max_y, max_x = stdscr.getmaxyx()
        height = len(help_lines) + 2
        width = max(len(line) for line in help_lines) + 4
        begin_y = max_y // 2 - height // 2
        begin_x = max_x // 2 - width // 2
        popup = curses.newwin(height, width, begin_y, begin_x)
        popup.bkgd(' ', curses.color_pair(2))
        popup.box()
        for i, line in enumerate(help_lines):
            try:
                popup.addstr(i + 1, 2, line, curses.color_pair(2))
            except curses.error:
                pass
        popup.refresh()
        popup.nodelay(0)
        popup.keypad(1)
        popup.getch()
        del popup