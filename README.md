# USB Passwd Tool (Linux) 🔥
Hey yo, welcome to my *USB Passwd Tool*! This lil beast makes crazy-long 64-char passwords, locks em up with a PIN, and slaps em on your clipboard—all from a USB drive. Built it for fun, maybe my thesis later. Let’s get it rollin’!

---

## What’s This Thing Do? 🎉
- **Spits Out Monster Passwords:** 64 chars of random madness—letters, numbers, symbols!
- **Keeps Em Safe:** PIN-locked, encrypted, only YOU get in.
- **Clipboard Magic:** Copies passwords so you can paste em anywhere.
- **Wipeout Mode:** 5 wrong PINs? Boom, it’s all gone.

---

## How to Run This Bad Boy 🚀
Follow these steps to fire it up on Linux. It’s easy, promise!

### Step 1: Grab the Code 🛒
- **Download It:** Click that green "Code" button up top and hit "Download ZIP".
- **Unzip It:** Toss it somewhere—like `/home/you/usb_password_tool`—or straight to a USB.
- **USB Vibes:** Wanna be cool? Plug in a USB, copy the folder to `/media/you/USBSTICK/` (check with `lsblk`).

### Step 2: Get Python Ready 🐍
- **Check It:** Open a terminal, type `python3 --version`. Got 3.6+? You’re golden.
- **No Python?** Run `sudo apt install python3` (Ubuntu/Debian) or whatever your distro needs.

### Step 3: Snag the Goodies 📦
- **Libs Time:** Cd to the folder (`cd /home/you/usb_password_tool` or your USB path).
- **Install Em:** Smash this in:
  ```bash
  python3 -m pip install cryptography pyperclip --target ./lib
