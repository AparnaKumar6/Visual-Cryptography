# Visual Cryptography Project

A Python implementation of (2,2) visual cryptography scheme that allows:
- Splitting an image into two noise-like shares
- Combining shares to reveal the original image
- Simple GUI for user interaction

## Features
- Binary image encryption/decryption
- Share generation and combination
- Simple GUI built with Tkinter

## Installation
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python gui.py`

## Usage
1. Click "Load Image" to select an image
2. Two shares will be generated automatically
3. Click "Combine Shares" to reconstruct the image
4. Save shares using the respective buttons

## Algorithm
The implementation uses a (2,2) visual cryptography scheme where:
- Each pixel is expanded to 2x2 subpixels
- White pixels use identical patterns in both shares
- Black pixels use complementary patterns
- When shares are superimposed, black pixels appear darker