from PIL import Image, ImageDraw, ImageFont
import numpy as np

def hide_text_in_image(image_path, text, key):
    """
    Hide text in an image by manipulating pixel values.

    Args:
    image_path (str): Path to the image file.
    text (str): Text to hide in the image.
    key (str): Encryption key.

    Returns:
    None
    """
    # Open the image
    img = Image.open(image_path)
    
    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Convert text to binary
    binary_text = ''.join(format(ord(char), '08b') for char in text)

    # Check if the image is large enough to hide the text
    if len(binary_text) > img_array.shape[0] * img_array.shape[1] * 3:
        raise Exception("Image is too small to hide the text.")

    # Hide the text in the image
    hidden_array = img_array.copy()
    index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(3):
                if index < len(binary_text):
                    # Hide the text in the least significant bit of each pixel
                    hidden_array[i, j, k] = (hidden_array[i, j, k] & ~1) | int(binary_text[index])
                    index += 1

    # Save the encrypted image
    encrypted_img = Image.fromarray(hidden_array)
    encrypted_img.save("encrypted_image.png")
    print("Text hidden and image encrypted successfully.")

def decrypt_image(encrypted_image_path, key):
    """
    Decrypt the encrypted image and retrieve the hidden text.

    Args:
    encrypted_image_path (str): Path to the encrypted image file.
    key (str): Encryption key.

    Returns:
    str: Retrieved text.
    """
    # Open the encrypted image
    encrypted_img = Image.open(encrypted_image_path)
    
    # Convert the encrypted image to a NumPy array
    encrypted_array = np.array(encrypted_img)

    # Retrieve the hidden text
    binary_text = ''
    for i in range(encrypted_array.shape[0]):
        for j in range(encrypted_array.shape[1]):
            for k in range(3):
                # Extract the least significant bit of each pixel
                binary_text += str(encrypted_array[i, j, k] & 1)

    # Convert binary text to string
    text = ''
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        if byte == '00000000':
            break
        text += chr(int(byte, 2))

    # Check if the key is correct
    if text[:len(key)] == key:
        # Create a new image with the retrieved text
        text_img = Image.new('RGB', (800, 600), color = (73, 109, 137))
        font = ImageFont.load_default()
        d = ImageDraw.Draw(text_img)
        d.text((10,10), text[len(key):], fill=(255,255,0), font=font)
        text_img.save("retrieved_text.png")
        print("Retrieved text saved to retrieved_text.png")
        return text[len(key):]
    else:
        print("Incorrect key. Text not decrypted.")
        return None

def main():
    print("Image Encryption and Decryption with Hidden Text")

    while True:
        print("\nOptions:")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            #image_path = 'C:\Users\HP\PRODIGY_INFOTECH\image1.png'. enter your image path as input
            image_path = input("Enter the path to the image file: ")
            text = input("Enter the text to hide: ")
            key = input("Enter the encryption key: ")
            hide_text_in_image(image_path, key + text, key)
        elif choice == "2":
            encrypted_image_path = "encrypted_image.png"
            key = input("Enter the encryption key: ")
            retrieved_text = decrypt_image(encrypted_image_path, key)
            if retrieved_text is not None:
                print("Retrieved text:", retrieved_text)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
