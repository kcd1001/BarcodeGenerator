import hashlib
from barcode import Code128
from barcode.writer import ImageWriter
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to generate a 9-digit hash
def generate_hash(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    hex_dig = hash_object.hexdigest()
    return str(int(hex_dig, 16))[:9]

# Function to generate a barcode from a product ID
def generate_barcode(product_id):
    hashed_id = generate_hash(product_id)
    barcode = Code128(hashed_id, writer=ImageWriter())
    barcode_filename = f'{product_id}.png'
    
    with open(barcode_filename, 'wb') as f:
        barcode.write(f)
    
    return barcode_filename

# Function to handle the button click event
def on_generate_button_click():
    product_id = entry.get()
    if product_id.strip():
        try:
            barcode_image_path = generate_barcode(product_id)
            display_barcode(barcode_image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate barcode: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter a valid Product ID.")

# Function to display the barcode image in the GUI
def display_barcode(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 150))  # Resize for display purposes
    img_tk = ImageTk.PhotoImage(img)
    
    barcode_label.config(image=img_tk)
    barcode_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to save the barcode image to a user-specified location
def save_barcode():
    product_id = entry.get()
    if product_id.strip():
        barcode_image_path = f'{product_id}.png'
        if barcode_image_path:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                with open(barcode_image_path, 'rb') as f_in, open(save_path, 'wb') as f_out:
                    f_out.write(f_in.read())
                messagebox.showinfo("Saved", f"Barcode saved to: {save_path}")
        else:
            messagebox.showwarning("Save Error", "No barcode generated to save.")
    else:
        messagebox.showwarning("Input Error", "Please enter a valid Product ID.")

# Set up the main GUI window
root = tk.Tk()
root.title("Barcode Generator")

# Product ID entry
tk.Label(root, text="Enter Product ID:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Generate Barcode button
generate_button = tk.Button(root, text="Generate Barcode", command=on_generate_button_click)
generate_button.pack(pady=10)

# Barcode display area
barcode_label = tk.Label(root)
barcode_label.pack(pady=10)

# Save Barcode button
save_button = tk.Button(root, text="Save Barcode", command=save_barcode)
save_button.pack(pady=10)

# Start the main event loop
root.mainloop()
