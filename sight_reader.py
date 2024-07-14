import customtkinter as ctk

class SightReadingTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create a frame for the camera view (16:9 aspect ratio)
        self.camera_frame = ctk.CTkFrame(self, fg_color="black")
        self.camera_frame.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8, relheight=0.45)

        # Ensure 16:9 aspect ratio
        self.camera_frame.bind("<Configure>", self.maintain_aspect_ratio)

        # Create a circular button in the bottom-right corner of the camera feed
        camera_button = ctk.CTkButton(self.camera_frame, text="", width=30, height=30, 
                                    corner_radius=15, fg_color="grey", 
                                    hover_color="dark grey", 
                                    command=self.camera_button_click)
        camera_button.place(relx=0.97, rely=0.95, anchor="se")

        # Create a frame for the sliders
        slider_frame = ctk.CTkFrame(self)
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

    def maintain_aspect_ratio(self, event):
        height = self.camera_frame.winfo_height()
        width = int(height * 16 / 9)
        self.camera_frame.configure(width=width)

    def camera_button_click(self):
        print("Camera button clicked!")