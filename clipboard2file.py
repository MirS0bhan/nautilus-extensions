import gi
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
from gi.repository import Nautilus, GObject, GLib, Gdk

from pathlib import Path
from typing import List


class ParchNautilusMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        menuitem = Nautilus.MenuItem(
            name="ParchNautilusMenuProvider::Paste2File",
            label="Paste to File",
            tip="Pastes clipboard content to a file named 'New File.txt'",
            icon="edit-paste",
        )

        menuitem.connect("activate", self.on_activate_paste_2_file, current_folder)
        return [menuitem]

    def on_activate_paste_2_file(self, menu_item, current_folder):
        # Get the clipboard contents asynchronously
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.read_text_async(None, self.on_paste_text, current_folder)

    def on_paste_text(self, clipboard, result, current_folder):
        # Finish reading the clipboard text
        text = clipboard.read_text_finish(result)
        if text is not None:
            # Get the directory from the selected folder
            directory = Path(current_folder.get_location().get_path())
            new_file_path = directory.joinpath("New File.txt").exists()
            if new_file_path.
            # Write the clipboard contents to the new file
            with open(new_file_path, 'w') as new_file:
                new_file.write(text)

            # Optionally, notify the user by opening the new file
            GLib.spawn_command_line_async(f'xdg-open "{new_file_path}"')

