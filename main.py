import customtkinter as ctk
from music21 import converter, note
import serial
import time
from songs_to_go import SongSelectionTab
from sight_reader import SightReadingTab

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Mozart App")
        self.master.geometry("800x700")  # Set a default window size
        
        self.current_index = -1
        self.songs = [
            {"name": "Twinkle Twinkle Little Star", "file": "Twinkle Twinkle Little Star.mxl"},
            {"name": "Jingle Bells", "file": "Jingle Bells.mxl"},
            {"name": "Yankee Doodle", "file": "Yankee Doodle.mxl"},
            {"name": "Happy Birthday", "file": "Happy Birthday.mxl"},
            {"name": "C Major", "file": "C Major.mxl"},
            {"name": "Every Note", "file": "Every Note.mxl"},
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
        
        self.sight_reading_tab = SightReadingTab(self.tab2, self.button_click)  # Replace setup_tab2() with this
        self.sight_reading_tab.pack(fill="both", expand=True)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.bottom_bar = ctk.CTkFrame(self.master, height=0)
        self.bottom_bar.pack(side="bottom", fill="x")
        
        self.button = ctk.CTkButton(self.bottom_bar, text="Play Song", command=self.button_click, bg_color="transparent")
        self.button.pack(expand=True, pady=(15, 25))

    def set_song(self, index):
        self.current_index = index
        print(f"Setting song to {self.current_index}: {self.songs[self.current_index]['name']}: {self.songs[self.current_index]['file']}")
        self.song_selection_tab.update_button_colors(self.current_index)

    def camera_button_click(self):
        print("Camera button clicked!")

    def button_click(self, other=False):
        if (self.current_index == -1 and other == False):
            print("[ERROR] No song selected")
        else:
            print(f"Playing song {self.current_index}: {self.songs[self.current_index]['name']}: {self.songs[self.current_index]['file']}")
            score = ""
            if (self.current_index < len(self.song_selection_tab.buttons) and other == False):
                score = converter.parse(f"songs/{self.songs[self.current_index]['file']}")
            else:
                score = converter.parse(f"new_song/temp.mxl")
            # score = converter.parse(f"songs/{self.songs[self.current_index]['file']}")
            

            string = "S"

            # Iterate through all the notes in the score
            for element in score.recurse().notes:
                if isinstance(element, note.Note):
                    string += f"{element.octave},{element.name.lower()},{round(element.quarterLength*1000)}\n"  
                    # print(element.name)
                    print(f'Note: {element.nameWithOctave}, Duration: {element.quarterLength}, Offset: {element.offset}')
                elif isinstance(element, note.Rest):
                    string += f"4,r,{round(element.quarterLength*1000)}\n"
                    print(f'Rest, Duration: {element.quarterLength}, Offset: {element.offset}')
            
            string += "|"
            print("Finished reading file")
            print("Sending data to Arduino")
            print(string)
            ser = serial.Serial('COM3', 115200)
            time.sleep(5)
            # send over the string in 10 character chunks
            # ser.write(b'S')
            for i in range(0, len(string), 10):
                ser.write(string[i:i+10].encode('utf-8'))
                time.sleep(0.1)
            # print(string.encode('utf-8'))
            # ser.write(string.encode('utf-8'))
            time.sleep(1)
            # printout all the data that is read from the serial port
            # stop while loop after 100 seconds
            tim = 0
            i = 0
            # while True:
            #     data = ser.readline()
            #     try:
            #         print(f"Read {i}: {data.decode()}", end="")
            #     except Exception:
            #         print(f"Read {i}: {data}", end="")
            #     # print(data.decode())
            #     i += 1
            #     time.sleep(0.1)
            #     tim += 0.1
            #     if tim > 100:
            #         break
            ser.close()

            print("Finished sending data")


            # self.play_song(self.songs[self.current_index]['file'])
        # print("Button clicked!")
    
    def on_closing(self):
        if hasattr(self.sight_reading_tab, 'on_closing'):
            self.sight_reading_tab.on_closing()
        self.master.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()