import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image # type: ignore
from vcrypt import VisualCryptography

class VCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Cryptography Tool")
        self.vc = VisualCryptography()
        
        # GUI Elements
        self.create_widgets()
    
    def create_widgets(self):
        # Input Image
        tk.Label(self.root, text="Original Image:").grid(row=0, column=0, padx=5, pady=5)
        self.original_img_label = tk.Label(self.root)
        self.original_img_label.grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Load Image", command=self.load_image).grid(row=2, column=0, padx=5, pady=5)
        
        # Share 1
        tk.Label(self.root, text="Share 1:").grid(row=0, column=1, padx=5, pady=5)
        self.share1_label = tk.Label(self.root)
        self.share1_label.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Save Share 1", command=lambda: self.save_image(self.share1)).grid(row=2, column=1, padx=5, pady=5)
        
        # Share 2
        tk.Label(self.root, text="Share 2:").grid(row=0, column=2, padx=5, pady=5)
        self.share2_label = tk.Label(self.root)
        self.share2_label.grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Save Share 2", command=lambda: self.save_image(self.share2)).grid(row=2, column=2, padx=5, pady=5)
        
        # Reconstructed Image
        tk.Label(self.root, text="Reconstructed Image:").grid(row=3, column=1, padx=5, pady=5)
        self.reconstructed_label = tk.Label(self.root)
        self.reconstructed_label.grid(row=4, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Combine Shares", command=self.combine_shares).grid(row=5, column=1, padx=5, pady=5)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            try:
                self.original_image = self.vc.image_to_binary(file_path)
                self.share1, self.share2 = self.vc.generate_shares(self.original_image)
                
                # Display images
                self.display_image(Image.fromarray(self.original_image), self.original_img_label)
                self.display_image(self.share1, self.share1_label)
                self.display_image(self.share2, self.share2_label)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
    
    def combine_shares(self):
        if hasattr(self, 'share1') and hasattr(self, 'share2'):
            reconstructed = self.vc.combine_shares(self.share1, self.share2)
            self.display_image(reconstructed, self.reconstructed_label)
        else:
            messagebox.showwarning("Warning", "Please load and generate shares first")
    
    def display_image(self, image, label_widget):
        # Resize for display
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)
        label_widget.config(image=photo)
        label_widget.image = photo  # Keep reference
    
    def save_image(self, image):
        if image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = VCryptApp(root)
    root.mainloop()