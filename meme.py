import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import platform
from tkinter import font as tkFont
from datetime import datetime

class MemeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator")
        self.root.geometry("800x600")
        
        # Constants
        self.TARGET_SIZE = (600, 600)
        
        # Create memes directory
        self.memes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "created_memes")
        if not os.path.exists(self.memes_dir):
            os.makedirs(self.memes_dir)
        
        # Variables
        self.image_path = tk.StringVar()
        self.top_text = tk.StringVar()
        self.bottom_text = tk.StringVar()
        self.font_size = tk.StringVar(value="50")
        self.selected_font = tk.StringVar()
        self.top_align = tk.StringVar(value="center")
        self.bottom_align = tk.StringVar(value="center")
        
        # Get available system fonts
        self.available_fonts = self.get_available_fonts()
        if self.available_fonts:
            self.selected_font.set(self.available_fonts[0])
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image selection
        ttk.Label(main_frame, text="Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, columnspan=2, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_image).grid(row=0, column=3, padx=5, pady=5)
        
        # Font settings frame
        font_frame = ttk.LabelFrame(main_frame, text="Font Settings", padding="5")
        font_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # Font selection
        ttk.Label(font_frame, text="Font:").grid(row=0, column=0, sticky=tk.W, padx=5)
        font_combo = ttk.Combobox(font_frame, textvariable=self.selected_font, values=self.available_fonts)
        font_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Font size
        ttk.Label(font_frame, text="Font Size:").grid(row=0, column=2, sticky=tk.W, padx=5)
        size_spinbox = ttk.Spinbox(font_frame, from_=10, to=200, textvariable=self.font_size, width=5)
        size_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Top text frame
        top_frame = ttk.LabelFrame(main_frame, text="Top Text", padding="5")
        top_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Top text input and alignment
        ttk.Entry(top_frame, textvariable=self.top_text, width=50).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Top text alignment
        ttk.Label(top_frame, text="Alignment:").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(top_frame, text="Left", variable=self.top_align, value="left").grid(row=1, column=1, padx=5)
        ttk.Radiobutton(top_frame, text="Center", variable=self.top_align, value="center").grid(row=1, column=2, padx=5)
        ttk.Radiobutton(top_frame, text="Right", variable=self.top_align, value="right").grid(row=1, column=3, padx=5)
        
        # Bottom text frame
        bottom_frame = ttk.LabelFrame(main_frame, text="Bottom Text", padding="5")
        bottom_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Bottom text input and alignment
        ttk.Entry(bottom_frame, textvariable=self.bottom_text, width=50).grid(row=0, column=0, columnspan=3, pady=5)
        
        # Bottom text alignment
        ttk.Label(bottom_frame, text="Alignment:").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(bottom_frame, text="Left", variable=self.bottom_align, value="left").grid(row=1, column=1, padx=5)
        ttk.Radiobutton(bottom_frame, text="Center", variable=self.bottom_align, value="center").grid(row=1, column=2, padx=5)
        ttk.Radiobutton(bottom_frame, text="Right", variable=self.bottom_align, value="right").grid(row=1, column=3, padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=20)
        
        # Generate button
        ttk.Button(button_frame, text="Generate Meme", command=self.generate_meme).grid(row=0, column=0, padx=5)
        
        # Open memes folder button
        ttk.Button(button_frame, text="Open Memes Folder", command=self.open_memes_folder).grid(row=0, column=1, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=5, column=0, columnspan=4)

    def get_available_fonts(self):
        system_fonts = sorted(tkFont.families())
        fonts = ['impact']
        fonts.extend([f for f in system_fonts if f.lower() not in ['impact']])
        return fonts

    def browse_image(self):
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Open an image',
            initialdir='/',
            filetypes=filetypes
        )
        if filename:
            self.image_path.set(filename)

    def open_memes_folder(self):
        """Open the created_memes folder in file explorer"""
        if not os.path.exists(self.memes_dir):
            messagebox.showerror("Error", "Memes folder not found!")
            return
            
        try:
            if platform.system() == 'Windows':  # Windows
                os.startfile(self.memes_dir)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{self.memes_dir}"')
            else:  # Linux/Unix
                os.system(f'xdg-open "{self.memes_dir}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open memes folder: {str(e)}")
            
    def get_text_size(self, text, font):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def resize_image(self, img):
        aspect_ratio = img.width / img.height
        
        if aspect_ratio > 1:
            new_width = self.TARGET_SIZE[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.TARGET_SIZE[1]
            new_width = int(new_height * aspect_ratio)
            
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        background = Image.new('RGB', self.TARGET_SIZE, 'white')
        paste_x = (self.TARGET_SIZE[0] - new_width) // 2
        paste_y = (self.TARGET_SIZE[1] - new_height) // 2
        
        background.paste(img, (paste_x, paste_y))
        return background

    def calculate_text_position(self, text_width, img_width, position_y, alignment):
        if alignment == "left":
            return 20, position_y  # 20 pixels padding from left
        elif alignment == "right":
            return img_width - text_width - 20, position_y  # 20 pixels padding from right
        else:  # center
            return (img_width - text_width) // 2, position_y

    def generate_meme(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        try:
            # Open and resize the image
            img = Image.open(self.image_path.get())
            img = self.resize_image(img)
            
            # Create drawing object
            draw = ImageDraw.Draw(img)
            
            # Get font size from input
            font_size = int(self.font_size.get())
            
            # Load selected font
            try:
                font = ImageFont.truetype(self.selected_font.get(), font_size)
            except:
                messagebox.showwarning("Font Warning", 
                    f"Could not load font '{self.selected_font.get()}'. Using default font instead.")
                font = ImageFont.load_default()
            
            def wrap_text(text):
                return textwrap.fill(text.upper(), width=20)
            
            # Process top text
            wrapped_top_text = wrap_text(self.top_text.get())
            top_text_width, top_text_height = self.get_text_size(wrapped_top_text, font)
            top_y = img.height // 15
            top_x, top_y = self.calculate_text_position(
                top_text_width, img.width, top_y, self.top_align.get())
            
            # Process bottom text
            wrapped_bottom_text = wrap_text(self.bottom_text.get())
            bottom_text_width, bottom_text_height = self.get_text_size(wrapped_bottom_text, font)
            bottom_y = img.height - bottom_text_height - img.height // 15
            bottom_x, bottom_y = self.calculate_text_position(
                bottom_text_width, img.width, bottom_y, self.bottom_align.get())
            
            def draw_text_with_border(text, position):
                border_width = 2
                for adj in range(-border_width, border_width+1):
                    for adj2 in range(-border_width, border_width+1):
                        draw.text((position[0]+adj, position[1]+adj2), 
                                text, font=font, fill='black')
                draw.text(position, text, font=font, fill='white')
            
            # Draw the text
            draw_text_with_border(wrapped_top_text, (top_x, top_y))
            draw_text_with_border(wrapped_bottom_text, (bottom_x, bottom_y))
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = os.path.splitext(os.path.basename(self.image_path.get()))[0]
            output_filename = f"meme_{original_filename}_{timestamp}.png"
            output_path = os.path.join(self.memes_dir, output_filename)
            
            # Save the meme
            img.save(output_path)
            
            self.status_label.config(text=f"Meme saved as: {output_filename}")
            messagebox.showinfo("Success", "Meme generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGeneratorApp(root)
    root.mainloop()