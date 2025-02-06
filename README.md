# Anki Flashcard Creator – Quick Start Guide

Welcome to the Anki Flashcard Creator! This tool lets you create vetically occluded Anki flashcards and automatically uploading them to your Anki decks. If you’re not a programmer, follow these simple steps to get started.

# How to Download and Run the Tool

Option 1: Download the Standalone Executable

If you don’t have Python installed or don’t want to install any extra software, we have built a standalone version of the tool for Windows.

    Download the Executable:
        Go to the Releases page on our GitHub repository.
        Download the file named something like anki_flashcard_creator.exe.

    Run the Application:
        Double-click the downloaded .exe file.
        The tool’s window will open.
        Note: If you see a security warning, click “Run” or “Allow” to continue.

    Using the Tool:
        Input Image: Choose either “Paste from Clipboard” (copy an image, then click the option) or “Load from File” to select an image saved on your computer.
        Deck Selection: Choose the Anki deck you want to add the cards to from the drop-down menu.
        Tags: Enter any tags you’d like to assign to the cards. (These tags stay the same until you change them.)
        Stripe Settings: Adjust the stripe color, stripe width (between 1% and 10%), and the number of stripes for each of the 3 cards.
        Create Cards: Click the "Process and Create Anki Cards" button. The tool will automatically create the cards and update the status message at the bottom of the window.

Option 2: Run from Source (For Advanced Users)

If you prefer to run the program from the source code, follow these steps:

    Download and Install Python:
        Download Python (version 3.9 or later) from python.org and install it.
        Make sure to check the box “Add Python to PATH” during installation.

    Download the Source Code:
        Clone the repository from GitHub or download the ZIP file from the repository page.

    Install Dependencies:
        honestly I have no clue what the dependencies are, as I made this tool entirely using AIstudio, chatgpt, deepseek... 
        I know Pillow is one, I know pyinstaller is another, rest is up to you, but if I could do it, I'm sure you can too. 

Run the Application:

    In the same terminal, run:

python anki_flashcard_creator.py

The application window will open, and you can use it as described above.
