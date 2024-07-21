import customtkinter as ctk
import cv2
from PIL import Image
import numpy as np
import os
import comtypes.client
import subprocess
from music21 import converter, note

class SightReadingTab(ctk.CTkFrame):
    def __init__(self, parent, button_click):
        super().__init__(parent)
        self.setup_ui()
        self.is_scanning = False
        self.scanned_image = None
        self.send_song = button_click
        self.processed_image = None

    def setup_ui(self):
        # Camera frame setup
        self.camera_frame = ctk.CTkFrame(self, fg_color="black")
        self.camera_frame.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.8, relheight=0.45)

        self.camera_label = ctk.CTkLabel(self.camera_frame, text="")
        self.camera_label.place(relx=0.5, rely=0.5, anchor="center")

        self.camera_frame.bind("<Configure>", self.maintain_aspect_ratio)

        # Camera button with transparent background and click effect
        self.camera_button = ctk.CTkButton(self.camera_frame, text="📷", width=40, height=40, 
                                    corner_radius=20, fg_color="transparent", 
                                    hover_color="gray70", 
                                    command=self.camera_button_click)
        self.camera_button.place(relx=0.97, rely=0.95, anchor="se")

        # Slider frame
        slider_frame = ctk.CTkFrame(self)
        slider_frame.place(relx=0.5, rely=0.75, anchor="center", relwidth=0.8, relheight=0.4)

        # Create sliders
        self.sliders = {}
        sliders_info = [
            ("Brightness", -100, 100, 0),
            ("Contrast", 0.5, 2.0, 1.0),
            ("Saturation", 0, 2, 1),
            ("Hue", 0, 180, 0),
            ("Sharpness", 0, 5, 1),
            ("Zoom", 1, 2, 1)
        ]

        for i, (name, min_val, max_val, default) in enumerate(sliders_info):
            row = i // 2
            col = i % 2

            label = ctk.CTkLabel(slider_frame, text=name)
            label.grid(row=row*2, column=col, padx=10, pady=(10,0), sticky="sw")
            
            slider = ctk.CTkSlider(slider_frame, from_=min_val, to=max_val, number_of_steps=100, command=self.update_image)
            slider.set(default)
            slider.grid(row=row*2+1, column=col, padx=10, pady=(0,10), sticky="ew")
            
            self.sliders[name.lower()] = slider

        # Configure the grid
        for i in range(3):
            slider_frame.grid_rowconfigure(i*2+1, weight=1)
        for i in range(2):
            slider_frame.grid_columnconfigure(i, weight=1)

    def maintain_aspect_ratio(self, event):
        height = self.camera_frame.winfo_height()
        width = int(height * 16 / 9)
        self.camera_frame.configure(width=width)
        self.camera_label.configure(width=width, height=height)

    def camera_button_click(self):
        if not self.is_scanning:
            self.scan_image()
            self.is_scanning = True
            self.camera_button.configure(text="▶️")
        else:
            self.process_image()
            self.is_scanning = False
            self.camera_button.configure(text="📷")

    def scan_image(self):
        wia = comtypes.client.CreateObject("WIA.DeviceManager")
        for device in wia.DeviceInfos:
            if device.Type == 1:  # Type 1 is for scanners
                scanner = device.Connect()
                break
        else:
            print("No scanner found.")
            return

        item = scanner.Items[1]
        item.Properties("6146").Value = 1  # Set to black and white

        image = item.Transfer()
        if os.path.exists('new_song/scanned_image.jpg'):
            os.remove('new_song/scanned_image.jpg')
        image.SaveFile('new_song/scanned_image.jpg')

        img = cv2.imread('new_song/scanned_image.jpg')
        rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite('new_song/scanned_image_rotated.jpg', rotated)

        self.scanned_image = cv2.imread('new_song/scanned_image_rotated.jpg')
        self.processed_image = self.scanned_image.copy()
        self.display_image(self.processed_image)
        

    def display_image(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (640, 360))
        image = Image.fromarray(frame_resized)
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(640, 360))
        self.camera_label.configure(image=ctk_image)
        self.camera_label.image = ctk_image

    def apply_video_effects(self, frame):
        # Apply brightness and contrast
        brightness = self.sliders['brightness'].get()
        contrast = self.sliders['contrast'].get()
        frame = cv2.addWeighted(frame, contrast, frame, 0, brightness)

        # Apply saturation
        saturation = self.sliders['saturation'].get()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(hsv)
        s = s * saturation
        s = np.clip(s, 0, 255)
        hsv = cv2.merge([h, s, v])
        frame = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

        # Apply hue shift
        hue_shift = int(self.sliders['hue'].get())
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,0] = (hsv[:,:,0] + hue_shift) % 180
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # Apply sharpness
        sharpness = self.sliders['sharpness'].get()
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) * sharpness
        frame = cv2.filter2D(frame, -1, kernel)

        # Apply zoom
        zoom = self.sliders['zoom'].get()
        h, w = frame.shape[:2]
        crop_h, crop_w = int(h / zoom), int(w / zoom)
        start_row, start_col = int((h - crop_h) / 2), int((w - crop_w) / 2)
        frame = frame[start_row:start_row+crop_h, start_col:start_col+crop_w]
        frame = cv2.resize(frame, (w, h))

        return frame

    def update_image(self, value):
        if self.scanned_image is not None:
            self.processed_image = self.apply_video_effects(self.scanned_image.copy())
            self.display_image(self.processed_image)

    def process_image(self):
        if self.processed_image is not None:
            cv2.imwrite('new_song/processed_image.jpg', self.processed_image)
            self.convert_image_to_mxl('new_song/processed_image.jpg', 'new_song')
            self.read_mxl_file()

    def convert_image_to_mxl(self, image_path, output_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('temp.png', gray)
        
        subprocess.run(['audiveris', '-force', '-batch', '-export', '-output', output_path, 'temp.png'], shell=True)
        
        os.remove('temp.png')

    def read_mxl_file(self):
        self.send_song(True)
        score = converter.parse('new_song/temp.mxl')
        for element in score.recurse().notes:
            if isinstance(element, note.Note):
                print(f'{element.octave}, {element.name.lower()}, {element.quarterLength}')
            elif isinstance(element, note.Rest):
                print(f'Rest, {element.quarterLength}')

    def on_closing(self):
        pass