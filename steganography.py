from PIL import Image
import numpy as np
import math

class ImageSteganography:
    def __init__(self):
        self.bits_used = 1  # Number of LSBs to use (1-4)
    
    def set_bits_used(self, bits):
        """Set how many least significant bits to use (1-4)"""
        if 1 <= bits <= 4:
            self.bits_used = bits
        else:
            raise ValueError("Bits must be between 1 and 4")
    
    def text_to_binary(self, text):
        """Convert text to binary string"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        # Add delimiter to mark end of message
        binary += '00000000'  # Null character as delimiter
        return binary
    
    def binary_to_text(self, binary):
        """Convert binary string to text"""
        text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if byte == '00000000':  # Stop at delimiter
                break
            text += chr(int(byte, 2))
        return text
    
    def encode_image(self, image_path, secret_text, output_path):
        """
        Encode secret text into an image
        """
        # Open the image
        img = Image.open(image_path)
        
        # Convert image to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert image to numpy array
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Convert text to binary
        binary_secret = self.text_to_binary(secret_text)
        
        # Calculate maximum capacity
        max_capacity = height * width * channels * self.bits_used
        if len(binary_secret) > max_capacity:
            raise ValueError(f"Message too large. Max capacity: {max_capacity} bits")
        
        # Flatten the array for easier processing
        flat_array = img_array.flatten()
        
        # Encode the message
        secret_index = 0
        for i in range(len(flat_array)):
            if secret_index >= len(binary_secret):
                break
            
            # Clear the specified number of LSBs
            flat_array[i] = flat_array[i] & (255 << self.bits_used)
            
            # Get bits to hide
            bits_to_hide = binary_secret[secret_index:secret_index + self.bits_used]
            bits_to_hide = bits_to_hide.ljust(self.bits_used, '0')
            
            # Insert the bits
            flat_array[i] |= int(bits_to_hide, 2)
            secret_index += self.bits_used
        
        # Reshape back to original dimensions
        encoded_array = flat_array.reshape((height, width, channels))
        
        # Create new image
        encoded_img = Image.fromarray(encoded_array.astype('uint8'))
        encoded_img.save(output_path)
        
        return True
    
    def decode_image(self, image_path):
        """
        Decode secret text from an image
        """
        # Open the image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Flatten the array
        flat_array = img_array.flatten()
        
        # Extract bits
        binary_message = ""
        bits_extracted = 0
        max_bits_to_extract = len(flat_array) * self.bits_used
        
        while bits_extracted < max_bits_to_extract:
            for i in range(0, len(flat_array), 1):
                if bits_extracted >= max_bits_to_extract:
                    break
                
                # Extract LSBs
                pixel_value = flat_array[i]
                extracted_bits = pixel_value & ((1 << self.bits_used) - 1)
                
                # Convert to binary string
                binary_message += format(extracted_bits, f'0{self.bits_used}b')
                bits_extracted += self.bits_used
                
                # Check if we have a complete byte and delimiter
                if len(binary_message) >= 8 and len(binary_message) % 8 == 0:
                    # Check for delimiter
                    last_byte = binary_message[-8:]
                    if last_byte == '00000000':
                        return self.binary_to_text(binary_message)
        
        # If no delimiter found, return what we have
        return self.binary_to_text(binary_message)
    
    def calculate_capacity(self, image_path):
        """
        Calculate maximum text capacity for an image
        """
        img = Image.open(image_path)
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Calculate bits available
        bits_available = height * width * channels * self.bits_used
        bytes_available = bits_available // 8
        chars_available = bytes_available - 1  # Account for delimiter
        
        return {
            'bits': bits_available,
            'bytes': bytes_available,
            'characters': chars_available,
            'image_dimensions': (width, height),
            'channels': channels
        }
    
    def compare_images(self, original_path, encoded_path):
        """
        Compare original and encoded images
        """
        original = Image.open(original_path)
        encoded = Image.open(encoded_path)
        
        original_array = np.array(original).flatten()
        encoded_array = np.array(encoded).flatten()
        
        # Calculate Mean Squared Error (MSE)
        mse = np.mean((original_array - encoded_array) ** 2)
        
        # Calculate Peak Signal-to-Noise Ratio (PSNR)
        if mse == 0:
            psnr = float('inf')
        else:
            max_pixel = 255.0
            psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
        
        # Calculate percentage of changed pixels
        changed_pixels = np.sum(original_array != encoded_array)
        total_pixels = len(original_array)
        change_percentage = (changed_pixels / total_pixels) * 100
        
        return {
            'mse': mse,
            'psnr': psnr,
            'changed_pixels': changed_pixels,
            'total_pixels': total_pixels,
            'change_percentage': change_percentage
        }