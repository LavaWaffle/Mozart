
import customtkinter as ctk

class SongSelectionTab(ctk.CTkFrame):
    def __init__(self, parent, songs, set_song_callback):
        super().__init__(parent)
        self.songs = songs
        self.set_song_callback = set_song_callback
        self.buttons = []
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)


        max_width = max(len(song['name']) for song in self.songs)
        button_width = max_width * 10
        for i in range(3):
            for j in range(0, 3, 2):
                button_index = i * 2 + j // 2
                button = ctk.CTkButton(
                    self, 
                    border_width=1, 
                    font=("Arial", 20),
                    text=f"{self.songs[button_index]['name']}", 
                    fg_color="#b145f5",  # Default color
                    hover_color="#a425f5",  # Hover color
                    border_color="#b145f5",  # Border color
                    command=lambda idx=button_index: self.set_song(idx),
                    width=button_width,  # Set fixed width for all buttons
                    height=55  # Set a fixed height for consistency
                )
                button.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=5, pady=5)
                self.buttons.append(button)  # Store button reference
       
        

    def set_song(self, index):
        self.set_song_callback(index)

    def update_button_colors(self, current_index):
        for i, button in enumerate(self.buttons):
            if i == current_index:
                button.configure(fg_color="#e14cf5", hover_color="#e14cf5")
            else:
                button.configure(fg_color="#b145f5", hover_color="#a425f5")