import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import steganography
import os

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.stego = steganography.ImageSteganography()
        self.current_image_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Encode Tab
        self.encode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encode_frame, text='Encode')
        self.setup_encode_tab()
        
        # Decode Tab
        self.decode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decode_frame, text='Decode')
        self.setup_decode_tab()
        
        # Settings Tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')
        self.setup_settings_tab()
    
    def setup_encode_tab(self):
        # Image selection
        ttk.Label(self.encode_frame, text="Cover Image:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.encode_image_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.encode_image_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_encode_image).grid(row=0, column=2, padx=5, pady=5)
        
        # Image preview
        self.encode_preview_label = ttk.Label(self.encode_frame, text="No image selected")
        self.encode_preview_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Secret message
        ttk.Label(self.encode_frame, text="Secret Message:").grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.secret_text = tk.Text(self.encode_frame, width=50, height=10)
        self.secret_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        # Character counter
        self.char_count_label = ttk.Label(self.encode_frame, text="Characters: 0")
        self.char_count_label.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        self.secret_text.bind('<KeyRelease>', self.update_char_count)
        
        # Output path
        ttk.Label(self.encode_frame, text="Output Image:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.output_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.output_path, width=50).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_output_image).grid(row=4, column=2, padx=5, pady=5)
        
        # Capacity info
        self.capacity_label = ttk.Label(self.encode_frame, text="Max capacity: N/A")
        self.capacity_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        
        # Encode button
        ttk.Button(self.encode_frame, text="Encode Message", 
                  command=self.encode_message, style='Accent.TButton').grid(row=6, column=0, columnspan=3, pady=20)
    
    def setup_decode_tab(self):
        # Image selection for decoding
        ttk.Label(self.decode_frame, text="Encoded Image:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.decode_image_path = tk.StringVar()
        ttk.Entry(self.decode_frame, textvariable=self.decode_image_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.decode_frame, text="Browse", command=self.browse_decode_image).grid(row=0, column=2, padx=5, pady=5)
        
        # Image preview
        self.decode_preview_label = ttk.Label(self.decode_frame, text="No image selected")
        self.decode_preview_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Decoded message
        ttk.Label(self.decode_frame, text="Decoded Message:").grid(row=2, column=0, padx=5, pady=5, sticky='nw')
        self.decoded_text = tk.Text(self.decode_frame, width=50, height=10, state='disabled')
        self.decoded_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        # Decode button
        ttk.Button(self.decode_frame, text="Decode Message", 
                  command=self.decode_message, style='Accent.TButton').grid(row=3, column=0, columnspan=3, pady=20)
        
        # Analysis section
        ttk.Label(self.decode_frame, text="Image Analysis:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.analysis_text = tk.Text(self.decode_frame, width=50, height=5, state='disabled')
        self.analysis_text.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
    
    def setup_settings_tab(self):
        # LSB selection
        ttk.Label(self.settings_frame, text="Number of LSBs to use:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.lsb_var = tk.IntVar(value=1)
        lsb_frame = ttk.Frame(self.settings_frame)
        lsb_frame.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        for i in range(1, 5):
            ttk.Radiobutton(lsb_frame, text=f"{i} bit{'s' if i > 1 else ''}", 
                           variable=self.lsb_var, value=i,
                           command=self.update_lsb_setting).pack(side='left', padx=5)
        
        # Information
        info_text = """
        Steganography Settings:
        
        • 1 LSB: Best invisibility, lower capacity
        • 2 LSBs: Good balance
        • 3 LSBs: Higher capacity, more visible changes
        • 4 LSBs: Maximum capacity, most visible
        
        Note: Encoder and decoder must use the same LSB setting!
        """
        
        info_label = ttk.Label(self.settings_frame, text=info_text, justify='left')
        info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky='w')
        
        # Reset button
        ttk.Button(self.settings_frame, text="Reset to Defaults",
                  command=self.reset_settings).grid(row=2, column=0, columnspan=2, pady=20)
    
    def browse_encode_image(self):
        filename = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if filename:
            self.encode_image_path.set(filename)
            self.show_image_preview(filename, self.encode_preview_label)
            self.update_capacity_info(filename)
    
    def browse_decode_image(self):
        filename = filedialog.askopenfilename(
            title="Select encoded image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if filename:
            self.decode_image_path.set(filename)
            self.show_image_preview(filename, self.decode_preview_label)
    
    def browse_output_image(self):
        filename = filedialog.asksaveasfilename(
            title="Save encoded image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def show_image_preview(self, image_path, label):
        try:
            img = Image.open(image_path)
            # Resize for preview
            img.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo, text="")
            label.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image: {str(e)}")
    
    def update_capacity_info(self, image_path):
        try:
            capacity = self.stego.calculate_capacity(image_path)
            info = (f"Max capacity: {capacity['characters']} characters "
                   f"({capacity['bytes']} bytes)\n"
                   f"Image: {capacity['image_dimensions'][0]}x{capacity['image_dimensions'][1]}, "
                   f"{capacity['channels']} channels")
            self.capacity_label.config(text=info)
        except Exception as e:
            self.capacity_label.config(text=f"Error calculating capacity: {str(e)}")
    
    def update_char_count(self, event=None):
        text = self.secret_text.get("1.0", "end-1c")
        self.char_count_label.config(text=f"Characters: {len(text)}")
    
    def encode_message(self):
        if not self.encode_image_path.get():
            messagebox.showerror("Error", "Please select a cover image")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify output path")
            return
        
        secret_text = self.secret_text.get("1.0", "end-1c")
        if not secret_text:
            messagebox.showerror("Error", "Please enter a secret message")
            return
        
        try:
            # Update LSB setting
            self.stego.set_bits_used(self.lsb_var.get())
            
            # Encode the message
            self.stego.encode_image(
                self.encode_image_path.get(),
                secret_text,
                self.output_path.get()
            )
            
            # Compare images
            comparison = self.stego.compare_images(
                self.encode_image_path.get(),
                self.output_path.get()
            )
            
            # Show success message with stats
            stats = (f"Message encoded successfully!\n\n"
                    f"Statistics:\n"
                    f"• MSE: {comparison['mse']:.4f}\n"
                    f"• PSNR: {comparison['psnr']:.2f} dB\n"
                    f"• Changed pixels: {comparison['change_percentage']:.2f}%")
            
            messagebox.showinfo("Success", stats)
            
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
    
    def decode_message(self):
        if not self.decode_image_path.get():
            messagebox.showerror("Error", "Please select an encoded image")
            return
        
        try:
            # Update LSB setting
            self.stego.set_bits_used(self.lsb_var.get())
            
            # Decode the message
            decoded = self.stego.decode_image(self.decode_image_path.get())
            
            # Display decoded message
            self.decoded_text.config(state='normal')
            self.decoded_text.delete("1.0", "end")
            self.decoded_text.insert("1.0", decoded)
            self.decoded_text.config(state='disabled')
            
            # Show analysis
            self.show_analysis()
            
        except Exception as e:
            messagebox.showerror("Decoding Error", str(e))
    
    def show_analysis(self):
        try:
            capacity = self.stego.calculate_capacity(self.decode_image_path.get())
            analysis = (f"Image Analysis:\n"
                       f"• Dimensions: {capacity['image_dimensions'][0]}x{capacity['image_dimensions'][1]}\n"
                       f"• Max capacity: {capacity['characters']} characters\n"
                       f"• LSBs used: {self.lsb_var.get()}")
            
            self.analysis_text.config(state='normal')
            self.analysis_text.delete("1.0", "end")
            self.analysis_text.insert("1.0", analysis)
            self.analysis_text.config(state='disabled')
            
        except Exception as e:
            self.analysis_text.config(state='normal')
            self.analysis_text.delete("1.0", "end")
            self.analysis_text.insert("1.0", f"Analysis error: {str(e)}")
            self.analysis_text.config(state='disabled')
    
    def update_lsb_setting(self):
        self.stego.set_bits_used(self.lsb_var.get())
        if self.encode_image_path.get():
            self.update_capacity_info(self.encode_image_path.get())
    
    def reset_settings(self):
        self.lsb_var.set(1)
        self.update_lsb_setting()
        messagebox.showinfo("Settings Reset", "Settings have been reset to defaults")

def main():
    root = tk.Tk()
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    app = SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()