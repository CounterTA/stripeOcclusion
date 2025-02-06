# Anki Flashcard Creator

Anki Flashcard Creator is a Python-based GUI application that allows users to create custom Anki flashcards by processing images. Users can add vertical stripes to images, choose the number of stripes per card, select the stripe color, set the stripe width, choose the target deck, and specify persistent tags for the cards. The application communicates with Anki via AnkiConnect.

## Features

- **Image Input:**  
  Users can either paste an image from the clipboard or load an image from a file.

- **Image Processing:**  
  The app adds vertical stripes to the image based on user-selected parameters:
  - Number of stripes for each of the 3 cards.
  - Stripe color (with a color chooser).
  - Stripe width limited between 1% and 10%.

- **Anki Integration:**  
  Uses AnkiConnect to:
  - Upload the original and processed images to Anki’s media collection.
  - Create flashcards with the processed images and user-defined tags.
  - Allow deck selection via a drop-down menu.

## Installation

### Prerequisites

- **AnkiConnect add-on**
- **Python 3.9 or later**  
- **Tkinter** (usually included with Python)  
- **Other dependencies:**  
  Install the required Python packages using pip:

```bash
pip install Pillow requests pyperclip
