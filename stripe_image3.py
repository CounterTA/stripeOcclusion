import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, UnidentifiedImageError, ImageGrab, ImageTk
import os
import io
import pyperclip
import requests  # For AnkiConnect
import time  # For unique filenames
import base64  # For image_to_base64

def create_anki_cards(original_image, striped_images, stripe_counts, stripe_color_hex, stripe_width_percent):
    """Automates Anki card creation using AnkiConnect with unique filenames."""
    # Get deck name from the deck selection widget (deck_var)
    deck_name = deck_var.get()
    # Get user-specified tags (if any); split by commas and strip whitespace.
    user_tags_str = tags_var.get()
    user_tags = [tag.strip() for tag in user_tags_str.split(",") if tag.strip()]
    
    model_name = "Basic"
    status_label.config(text="Creating Anki cards...")
    root.update()
    try:
        timestamp = str(int(time.time()))
        # 1. Store Original Image in Anki Media with unique filename
        original_filename = f'original_image_{timestamp}.png'
        anki_store_media(original_filename, image_to_base64(original_image))
        # 2. Store and Create Cards for Striped Images with unique filenames
        for i, num_stripes in enumerate(stripe_counts):
            striped_filename = f'stripes_{num_stripes}_{timestamp}.png'
            anki_store_media(striped_filename, image_to_base64(striped_images[i]))
            front_text = f"<img src='{striped_filename}'>"
            back_text = f"<p>Original Image:</p><img src='{original_filename}'>"
            # Use the user-specified tags (you can add extra tags here if desired)
            tags_list = user_tags
            anki_add_note(deck_name, model_name, front_text, back_text, tags_list)
        status_label.config(text="Anki cards created successfully!")
        # No pop-up; just update status_label.
    except Exception as e_anki:
        status_label.config(text="Anki card creation failed. See error message.")
        print(f"Anki Card Creation Error Details:\n{e_anki}")

def add_vertical_stripes(img, num_stripes, stripe_color, stripe_width_percentage):
    """Adds vertical stripes to a PIL Image object and returns the new Image object."""
    try:
        img_copy = img.copy()
        width, height = img_copy.size
        draw = ImageDraw.Draw(img_copy)
        stripe_width = int(width * stripe_width_percentage)
        if stripe_width < 1:
            stripe_width = 1
        space_between_stripes = (width - (num_stripes * stripe_width)) // (num_stripes + 1)
        current_x = space_between_stripes
        for _ in range(num_stripes):
            draw.rectangle([(current_x, 0), (current_x + stripe_width, height)], fill=stripe_color)
            current_x += stripe_width + space_between_stripes
        return img_copy
    except Exception as e:
        messagebox.showerror("Error", f"Stripe addition error: {e}")
        return None


def get_image_from_clipboard():
    """Retrieves an image from the clipboard, prioritizing ImageGrab."""
    try:
        img = ImageGrab.grabclipboard()
        if img:
            return img
    except Exception as e_imagegrab:
        print(f"ImageGrab error: {e_imagegrab}. Trying pyperclip fallback.")
    try:  # Fallback to pyperclip (less reliable for images)
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            try:
                image_bytes = io.BytesIO(clipboard_data.encode('utf-8'))
                img = Image.open(image_bytes)
                return img
            except Exception as e_bytes_io:
                messagebox.showerror("Clipboard Error", f"Error processing clipboard data: {e_bytes_io}")
        else:
            messagebox.showinfo("Clipboard Empty", "Clipboard is empty. Please copy an image to the clipboard first.")
    except Exception as e_general:
        messagebox.showerror("Clipboard Error", f"General clipboard error: {e_general}")
    return None


def load_image_from_file():
    """Opens a file dialog to load an image from a file."""
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"), ("All files", "*.*"))
    )
    if file_path:
        try:
            img = Image.open(file_path)
            return img
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading image: {e}")
    return None


def anki_store_media(filename, base64_data):
    """Stores media file in Anki using AnkiConnect."""
    params = {"action": "storeMediaFile", "version": 6, "params": {"filename": filename, "data": base64_data}}
    response = requests.post('http://127.0.0.1:8765', json=params).json()
    if response['error']:
        raise Exception(f"AnkiConnect storeMediaFile error: {response['error']}")
    return response['result']



def anki_add_note(deck_name, model_name, front_text, back_text, tags):
    """Adds a note to Anki using AnkiConnect."""
    fields = {"Front": front_text, "Back": back_text}
    note = {"deckName": deck_name, "modelName": model_name, "fields": fields, "options": {"allowDuplicate": False}, "tags": tags}
    params = {"action": "addNote", "version": 6, "params": {"note": note}}
    response = requests.post('http://127.0.0.1:8765', json=params).json()
    if response['error']:
        raise Exception(f"AnkiConnect addNote error: {response['error']}")
    return response['result']

def save_image_temp(image):
    """Saves a PIL image to a temporary file and returns its path."""
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_file, format="PNG")
    temp_file.close()
    return temp_file.name

def image_to_base64(img):
    """Converts a PIL Image to a base64 encoded string for Anki."""
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode()
    return base64_str

import base64 # Import base64 at the end as it's used in image_to_base64

def get_deck_names():
    """Fetch deck names from AnkiConnect; if it fails, return a default list."""
    try:
        response = requests.post('http://127.0.0.1:8765', json={"action": "deckNames", "version": 6}).json()
        if response['error'] is None:
            return response['result']
    except Exception as e:
        messagebox.showerror("AnkiConnect Error", f"Could not fetch deck names: {e}")
    return ["Image Stripes Deck"]

def process_and_create_cards():
    """Main function to get image, add stripes, and create Anki cards."""
    global original_image_pil  # To store the original image
    input_method = input_method_var.get()
    original_image_pil = None
    if input_method == "clipboard":
        original_image_pil = get_image_from_clipboard()
    elif input_method == "file":
        original_image_pil = load_image_from_file()
    if original_image_pil:
        try:
            stripe_color_hex = stripe_color_var.get()
            stripe_width_percent = stripe_width_scale.get() / 100.0
            # Get the stripe counts from the three spinboxes:
            stripe_counts = [
                int(card1_spin.get()),
                int(card2_spin.get()),
                int(card3_spin.get())
            ]
            striped_images_pil = []
            for num_stripes in stripe_counts:
                striped_img = add_vertical_stripes(original_image_pil, num_stripes, stripe_color_hex, stripe_width_percent)
                if striped_img:
                    striped_images_pil.append(striped_img)
                else:
                    return  # Stop if stripe addition fails
            if len(striped_images_pil) == len(stripe_counts):
                create_anki_cards(original_image_pil, striped_images_pil, stripe_counts, stripe_color_hex, stripe_width_percent)
        except Exception as e_process:
            messagebox.showerror("Processing Error", f"Error during image processing: {e_process}")
            status_label.config(text="Image processing failed.")
    else:
        status_label.config(text="No image loaded.")


def choose_stripe_color():
    """Opens a color chooser dialog and updates the stripe color variable."""
    color_code = colorchooser.askcolor(initialcolor=stripe_color_var.get())[1]
    if color_code:
        stripe_color_var.set(color_code)
        color_preview_label.config(bg=color_code)


# ----- GUI Setup -----
root = tk.Tk()
root.title("Anki Flashcard Creator")

input_method_var = tk.StringVar()
input_method_var.set("clipboard")
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
clipboard_radio = tk.Radiobutton(input_frame, text="Paste from Clipboard", variable=input_method_var, value="clipboard")
clipboard_radio.pack(side=tk.LEFT, padx=10)
file_radio = tk.Radiobutton(input_frame, text="Load from File", variable=input_method_var, value="file")
file_radio.pack(side=tk.LEFT, padx=10)

# Deck Selection (using AnkiConnect to get deck names)
deck_names = get_deck_names()
deck_var = tk.StringVar(value=deck_names[0])
deck_frame = tk.Frame(root)
deck_frame.pack(pady=10)
deck_label = tk.Label(deck_frame, text="Select Deck:")
deck_label.pack(side=tk.LEFT, padx=5)
deck_menu = tk.OptionMenu(deck_frame, deck_var, *deck_names)
deck_menu.pack(side=tk.LEFT, padx=5)

# Tags Entry (persistent tags)
tags_var = tk.StringVar(value="")  # Default empty; user can enter comma-separated tags.
tags_frame = tk.Frame(root)
tags_frame.pack(pady=10)
tags_label = tk.Label(tags_frame, text="Tags (comma-separated):")
tags_label.pack(side=tk.LEFT, padx=5)
tags_entry = tk.Entry(tags_frame, textvariable=tags_var, width=40)
tags_entry.pack(side=tk.LEFT, padx=5)

# Stripe customization frame
customization_frame = tk.Frame(root)
customization_frame.pack(pady=10)

# Stripe Color
stripe_color_label = tk.Label(customization_frame, text="Stripe Color:")
stripe_color_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
stripe_color_var = tk.StringVar(value="#000000")
color_preview_label = tk.Label(customization_frame, width=3, relief=tk.SOLID, bd=1, bg=stripe_color_var.get())
color_preview_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
choose_color_button = tk.Button(customization_frame, text="Choose Color", command=choose_stripe_color)
choose_color_button.grid(row=0, column=2, padx=5, pady=5)
# Stripe Width (limited between 1% and 10%)
stripe_width_label = tk.Label(customization_frame, text="Stripe Width (%):")
stripe_width_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
stripe_width_scale = tk.Scale(customization_frame, from_=1, to=10, orient=tk.HORIZONTAL, resolution=1, length=150)
stripe_width_scale.set(5)
stripe_width_scale.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")


# New frame for Card Stripe Counts
card_stripe_frame = tk.Frame(root)
card_stripe_frame.pack(pady=10)
card1_label = tk.Label(card_stripe_frame, text="Card 1 - Number of Stripes:")
card1_label.pack(side=tk.LEFT, padx=5)
card1_spin = tk.Spinbox(card_stripe_frame, from_=1, to=50, width=5)
card1_spin.delete(0, tk.END)
card1_spin.insert(0, "3")
card1_spin.pack(side=tk.LEFT, padx=5)
card2_label = tk.Label(card_stripe_frame, text="Card 2 - Number of Stripes:")
card2_label.pack(side=tk.LEFT, padx=5)
card2_spin = tk.Spinbox(card_stripe_frame, from_=1, to=50, width=5)
card2_spin.delete(0, tk.END)
card2_spin.insert(0, "6")
card2_spin.pack(side=tk.LEFT, padx=5)
card3_label = tk.Label(card_stripe_frame, text="Card 3 - Number of Stripes:")
card3_label.pack(side=tk.LEFT, padx=5)
card3_spin = tk.Spinbox(card_stripe_frame, from_=1, to=50, width=5)
card3_spin.delete(0, tk.END)
card3_spin.insert(0, "10")
card3_spin.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(root, text="Process and Create Anki Cards", command=process_and_create_cards, padx=20, pady=10)
process_button.pack(pady=20)
status_label = tk.Label(root, text="Ready")
status_label.pack(pady=5)
original_image_pil = None  # To store the original PIL image
root.mainloop()