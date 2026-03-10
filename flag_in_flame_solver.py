import sys
import base64
import re
import binascii
from PIL import Image
import pytesseract

def decode_base64_to_image(input_file):

    try:
        with open(input_file, "r") as f:
            data = f.read()

        decoded = base64.b64decode(data)

        image_file = "decoded_image.jpg"

        with open(image_file, "wb") as img:
            img.write(decoded)

        print("[SUCCESS] Image created:", image_file)

        return image_file

    except Exception as e:
        print("[ERROR] Base64 decoding failed:", e)
        return None


def extract_text_from_image(image_path):

    try:
        img = Image.open(image_path)

        text = pytesseract.image_to_string(img)

        print("\n[INFO] OCR Extracted Text:\n")
        print(text)

        return text

    except Exception as e:
        print("[ERROR] OCR failed:", e)
        return ""


def find_hex_string(text):

    # find hex sequences that may be separated by spaces
    hex_pattern = r'([0-9a-fA-F\s]{20,})'
    matches = re.findall(hex_pattern, text)

    for m in matches:
        cleaned = m.replace(" ", "").replace("\n", "")
        if len(cleaned) % 2 == 0:
            return cleaned

    return None


def hex_to_ascii(hex_string):

    try:
        decoded = binascii.unhexlify(hex_string).decode()
        return decoded
    except:
        return None


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 solver.py logs.txt")
        return

    logfile = sys.argv[1]

    print("[INFO] Reading Base64 log file...")

    image_path = decode_base64_to_image(logfile)

    if not image_path:
        return

    print("[INFO] Running OCR on image...")

    text = extract_text_from_image(image_path)

    print("\n[INFO] Searching for hex string...")

    hex_string = find_hex_string(text)

    if not hex_string:
        print("[INFO] No hex string found.")
        return

    print("[SUCCESS] Hex Found:", hex_string)

    print("[INFO] Converting hex → ASCII...")

    flag = hex_to_ascii(hex_string)

    if flag:
        print("\n[#]FLAG FOUND:")
        print(flag)
    else:
        print("[INFO] Hex decoding failed.")


if __name__ == "__main__":
    main()