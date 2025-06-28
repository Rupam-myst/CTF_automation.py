import os
import shutil
import subprocess
import requests
import zipfile
import re

# === Step 0: Get ZIP URL from user ===
url = input("-->Enter the ZIP file URL: ").strip()
zip_name = "challenge.zip"
extract_dir = "drop-in"

# === Step 1: Download ZIP file ===
print(f"[*] Downloading from {url} ...")
try:
    r = requests.get(url)
    r.raise_for_status()
    with open(zip_name, "wb") as f:
        f.write(r.content)
    print(f"[+] Downloaded: {zip_name}")
except Exception as e:
    print(f"❌ Failed to download ZIP: {e}")
    exit(1)

# === Step 2: Extract the ZIP ===
print("[*] Extracting...")
try:
    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall()
    print(f"[+] Extracted to: {extract_dir}/")
except Exception as e:
    print(f"❌ Failed to unzip: {e}")
    exit(1)

# === Step 3: Navigate and extract flag ===
try:
    os.chdir(extract_dir)
    print("[*] Checking git history...")
    result = subprocess.check_output(["git", "reflog"], stderr=subprocess.DEVNULL)
    output = result.decode("utf-8")
    match = re.search(r"picoCTF\{.*?\}", output)

    if match:
        flag = match.group(0)
        print(f"🏁 FLAG FOUND: {flag}")
        with open("flag.txt", "w") as f:
            f.write(flag + "\n")
        print("[*] Flag saved to flag.txt")
    else:
        print("❌ No flag found in git history.")
except Exception as e:
    print(f"❌ Error during git flag extraction: {e}")
finally:
    os.chdir("..")

# === Step 4: Cleanup ===
print("[*] Cleaning up...")
try:
    os.remove(zip_name)
    shutil.rmtree(extract_dir)
    print("[+] Removed ZIP and extracted folder.")
except Exception as e:
    print(f"⚠️ Cleanup failed: {e}")
