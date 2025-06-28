import pexpect
import time
import re

# === Configuration ===
ssh_host = "atlas.picoctf.net"
ssh_port = "64699"  # ⚠️ Make sure this is the current working port
ssh_user = "ctf-player"
ssh_password = "1ad5be0d"

flag_pattern = r"picoCTF\{.*?\}"

while True:
    print("\n[*] New session starting...")

    try:
        ssh_cmd = f"ssh -p {ssh_port} {ssh_user}@{ssh_host}"
        child = pexpect.spawn(ssh_cmd, encoding='utf-8', timeout=10)

        # === Handle SSH prompts
        i = child.expect([
            "Are you sure you want to continue connecting",
            "password:",
            pexpect.EOF,
            pexpect.TIMEOUT
        ])
        if i == 0:
            print("[+] Accepting host key...")
            child.sendline("yes")
            child.expect("password:")

        # === Enter password
        print("[+] Sending password...")
        child.sendline(ssh_password)

        # === Wait for game to start
        child.expect("Enter your guess:")
        print("[+] Game started!")

        # === Binary search
        low = 1
        high = 1000
        flag = None

        for attempt in range(10):
            guess = (low + high) // 2
            print(f"[+] Attempt {attempt + 1}: Guessing {guess}")
            child.sendline(str(guess))

            index = child.expect([
                "Higher! Try again.",
                "Lower! Try again.",
                "Congratulations! You guessed the correct number",
                pexpect.EOF,
                pexpect.TIMEOUT
            ])

            if index == 0:
                print("[Server]: Higher!")
                low = guess + 1
            elif index == 1:
                print("[Server]: Lower!")
                high = guess - 1
            elif index == 2:
                print("[Server]: Correct guess!")
                
                # Wait for flag line
                try:
                    child.expect("Here's your flag:", timeout=3)
                    child.expect(flag_pattern, timeout=3)
                    flag = child.after.strip()
                    print("🏁 FLAG FOUND:", flag)

                    # Save to file
                    with open("flag.txt", "w") as f:
                        f.write(flag + "\n")
                    print("[*] Flag saved to flag.txt")
                except Exception as e:
                    print("[!] Flag not found after success. Scanning buffer...")
                    combined_output = child.before + child.after
                    match = re.search(flag_pattern, combined_output)
                    if match:
                        flag = match.group(0)
                        print("🏁 FLAG FOUND via fallback:", flag)
                        with open("flag.txt", "w") as f:
                            f.write(flag + "\n")
                        print("[*] Flag saved to flag.txt")
                    else:
                        print("[!] Could not locate flag.")
                break
            else:
                print("[!] Connection dropped or timed out.")
                break

        child.close()

        if flag:
            break

        print("[*] Retrying in 2 seconds...")
        time.sleep(2)

    except Exception as e:
        print(f"[!] Error: {e}")
        print("[*] Retrying in 3 seconds...\n")
        time.sleep(3)
