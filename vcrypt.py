import numpy as np # type: ignore
from PIL import Image # type: ignore

class VisualCryptography:
    def __init__(self):
        # Define the patterns for white and black pixels
        self.white_patterns = [
            np.array([[1, 0], [1, 0]]),  # Share 1 pattern for white
            np.array([[1, 0], [1, 0]])   # Share 2 pattern for white
        ]
        self.black_patterns = [
            np.array([[1, 0], [1, 0]]),  # Share 1 pattern for black
            np.array([[0, 1], [0, 1]])   # Share 2 pattern for black
        ]
    
    def image_to_binary(self, image_path):
        """Convert image to binary (black and white)"""
        img = Image.open(image_path).convert('L')  # Convert to grayscale
        img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Threshold to binary
        return np.array(img)
    
    def generate_shares(self, binary_image):
        """Generate two shares from binary image"""
        height, width = binary_image.shape
        share1 = np.zeros((height * 2, width * 2), dtype=np.uint8)
        share2 = np.zeros((height * 2, width * 2), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                pixel = binary_image[i, j]
                # Select patterns based on pixel value
                if pixel == 255:  # White pixel
                    p1, p2 = self.white_patterns
                else:  # Black pixel
                    p1, p2 = self.black_patterns
                
                # Apply patterns to shares
                share1[i*2:(i+1)*2, j*2:(j+1)*2] = p1 * 255
                share2[i*2:(i+1)*2, j*2:(j+1)*2] = p2 * 255
        
        return Image.fromarray(share1), Image.fromarray(share2)
    
    def combine_shares(self, share1, share2):
        """Combine two shares to reconstruct the image"""
        share1_arr = np.array(share1)
        share2_arr = np.array(share2)
        
        # Simple OR operation to combine shares
        combined = np.bitwise_or(share1_arr, share2_arr)
        
        # Downsample to original size
        height, width = combined.shape
        reconstructed = np.zeros((height//2, width//2), dtype=np.uint8)
        
        for i in range(0, height, 2):
            for j in range(0, width, 2):
                # If any subpixel is black in the combined image, mark as black
                if np.any(combined[i:i+2, j:j+2] == 0):
                    reconstructed[i//2, j//2] = 0
                else:
                    reconstructed[i//2, j//2] = 255
        
        return Image.fromarray(reconstructed)