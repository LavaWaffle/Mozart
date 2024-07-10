import customtkinter as ctk
from music21 import converter, note
import serial
import time
from songs_to_go import SongSelectionTab

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Custom App")
        self.master.geometry("800x700")  # Set a default window size
        
        self.current_index = -1
        self.songs = [
            {"name": "Twinkle Twinkle Little Star", "file": "Twinkle Twinkle Little Star.mxl"},
            {"name": "Jingle Bells", "file": "jingle_bells.mxl"},
            {"name": "chula", "file": "chula.mxl"},
            {"name": "Yankee Doodle", "file": "yankee_doodle.mxl"},
            {"name": "C Major", "file": "c_major.mxl"},
            {"name": "Every Key", "file": "every_key.mxl"},
        ]
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, pady=(0, 0))
        
        self.tab1 = self.tabview.add("Songs to Go")
        self.tab2 = self.tabview.add("Sight Reading")
        
        self.song_selection_tab = SongSelectionTab(self.tab1, self.songs, self.set_song)
        self.song_selection_tab.pack(fill="both", expand=True)
        
        self.setup_tab2()
        
        self.bottom_bar = ctk.CTkFrame(self.master, height=0)
        self.bottom_bar.pack(side="bottom", fill="x")
        
        self.button = ctk.CTkButton(self.bottom_bar, text="Play Song", command=self.button_click, bg_color="transparent")
        self.button.pack(expand=True, pady=(15, 25))

    def set_song(self, index):
        self.current_index = index
        print(f"Setting song to {self.current_index}: {self.songs[self.current_index]['name']}: {self.songs[self.current_index]['file']}")
        self.song_selection_tab.update_button_colors(self.current_index)

    def setup_tab2(self):
        # Create a frame for the camera view (16:9 aspect ratio)
        camera_frame = ctk.CTkFrame(self.tab2, fg_color="black")
        camera_frame.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8, relheight=0.45)

        # Ensure 16:9 aspect ratio
        def maintain_aspect_ratio(event):
            height = camera_frame.winfo_height()
            width = int(height * 16 / 9)
            camera_frame.configure(width=width)
            # Recenter the frame
            # camera_frame.place(relx=0.5, rely=0.3, anchor="center", width=width, height=height)

        camera_frame.bind("<Configure>", maintain_aspect_ratio)

        # Create a circular button in the bottom-right corner of the camera feed
        camera_button = ctk.CTkButton(camera_frame, text="", width=30, height=30, 
                                    corner_radius=15, fg_color="grey", 
                                    hover_color="dark grey", 
                                    command=self.camera_button_click)
        camera_button.place(relx=0.97, rely=0.95, anchor="se")

        # Create a frame for the sliders
        slider_frame = ctk.CTkFrame(self.tab2)
        slider_frame.place(relx=0.5, rely=0.75, anchor="center", relwidth=0.8, relheight=0.4)

        # Create a 3x2 grid of sliders
        sliders = ["Brightness", "Contrast", "Saturation", "Hue", "Sharpness", "Zoom"]
        for i, slider_name in enumerate(sliders):
            row = i // 2
            col = i % 2

            label = ctk.CTkLabel(slider_frame, text=slider_name)
            label.grid(row=row*2, column=col, padx=10, pady=(10,0), sticky="sw")
            
            slider = ctk.CTkSlider(slider_frame, from_=0, to=100, number_of_steps=100)
            slider.grid(row=row*2+1, column=col, padx=10, pady=(0,10), sticky="ew")

        # Configure the grid
        for i in range(3):
            slider_frame.grid_rowconfigure(i*2+1, weight=1)
        for i in range(2):
            slider_frame.grid_columnconfigure(i, weight=1)

    def camera_button_click(self):
        print("Camera button clicked!")

    def button_click(self):
        if (self.current_index == -1):
            print("[ERROR] No song selected")
        elif (self.current_index < len(self.song_selection_tab.buttons)):
            print(f"Playing song {self.current_index}: {self.songs[self.current_index]['name']}: {self.songs[self.current_index]['file']}")
            
            score = converter.parse(self.songs[self.current_index]['file'])
            string = ""

            # Iterate through all the notes in the score
            for element in score.recurse().notes:
                if isinstance(element, note.Note):
                    string += f"3,{element.name.lower()},{round(element.quarterLength*1000)}\n"  
                    # print(element.name)
                    print(f'Note: {element.nameWithOctave}, Duration: {element.quarterLength}, Offset: {element.offset}')
                elif isinstance(element, note.Rest):
                    string += f"3,r,{round(element.quarterLength*1000)}\n"
                    print(f'Rest, Duration: {element.quarterLength}, Offset: {element.offset}')
            
            string += "|"
            print("Finished reading file")
            print("Sending data to Arduino")

            ser = serial.Serial('COM3', 9600)
            time.sleep(1)
            ser.write(string.encode())
            time.sleep(1)
            ser.close()

            print("Finished sending data")


            # self.play_song(self.songs[self.current_index]['file'])
        # print("Button clicked!")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()