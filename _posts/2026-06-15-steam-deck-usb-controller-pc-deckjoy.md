---
title: 'Using a Steam Deck as a Wired USB Controller for a Windows PC'
date: 2026-06-15
permalink: /posts/2026/06/steam-deck-usb-controller-pc-deckjoy/
tags:
  - Steam Deck
  - Windows
  - USB
  - Controller
  - DeckJoy
  - Linux
---

> The Steam Deck does not normally behave like a USB controller when plugged into a PC. With DeckJoy, however, the Deck can expose itself as a USB HID composite device: game controller, keyboard, and mouse. This post records the exact path we used to make it work on Windows, including the BIOS setting, SSH setup, DeckJoy install, verification, and the problems that came up along the way.

## Goal

The target setup was simple:

- Steam Deck connected directly to a Windows PC over USB-C.
- No Steam Remote Play.
- No network streaming.
- Windows should see the Deck as a local controller input device.

The important constraint is that USB-C by itself is not enough. The Deck must present a USB device profile to the PC. Stock SteamOS does not expose the built-in controls as a wired gamepad, so we used DeckJoy.

DeckJoy repo:

```text
https://github.com/Lucaber/deckjoy
```

Release used:

```text
https://github.com/Lucaber/deckjoy/releases/download/v0.4.0/deckjoy.zip
```

## What Finally Worked

The working path was:

1. Enable USB dual-role device mode in the Steam Deck firmware.
2. Install DeckJoy on the Steam Deck.
3. Start DeckJoy on the Deck.
4. Press **Start USB** inside DeckJoy.
5. Windows detects a new USB HID composite device.

After it worked, Windows showed:

```text
USB\VID_1D6B&PID_0104
USB Composite Device
HID-compliant game controller
HID Keyboard Device
HID-compliant mouse
```

On the Deck side, the USB gadget was active:

```text
/sys/kernel/config/usb_gadget/g.1/strings/0x409/product
  Steam Deck (DeckJoy)

/sys/kernel/config/usb_gadget/g.1/strings/0x409/manufacturer
  Valve

/sys/kernel/config/usb_gadget/g.1/idVendor
  0x1d6b

/sys/kernel/config/usb_gadget/g.1/idProduct
  0x0104

/dev/hidg0
/dev/hidg1
/dev/hidg2
```

## Step 1: Enable USB DRD Mode

DeckJoy needs the Deck's USB-C port to support device/gadget mode.

On the Steam Deck:

1. Fully shut down.
2. Hold `Volume Up`, then press `Power`.
3. Enter `Setup Utilities`.
4. Go to `Advanced` -> `USB Configuration` -> `USB Dual Role Device`.
5. Set it to `DRD`.
6. Save and exit.

Without this, Windows may only see charging behavior, or nothing useful at all.

## Step 2: Set a Deck Password and Enable SSH

This part is optional if you do everything directly on the Deck, but SSH made it much easier to copy files and inspect the system from the PC.

In Desktop Mode, open Konsole:

```bash
passwd
sudo systemctl enable --now sshd
```

Find the Deck IP:

```bash
ip -4 addr
```

In our case the Deck was reachable at:

```text
192.168.31.51
```

I used SSH key auth rather than putting the Deck password into shell commands. The public key goes into:

```bash
~/.ssh/authorized_keys
```

The filename matters. It is `authorized_keys`, not `auth_keys`.

Useful permissions:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
sudo systemctl restart sshd
```

## Step 3: Download DeckJoy

On the Deck, the direct download path is:

```bash
cd ~/Downloads
curl -L -o deckjoy.zip https://github.com/Lucaber/deckjoy/releases/download/v0.4.0/deckjoy.zip
unzip deckjoy.zip -d deckjoy
cd deckjoy
chmod +x deckjoy
```

In our session I copied the same release over SSH/SFTP from the Windows PC, but the result was identical:

```text
/home/deck/Downloads/deckjoy/deckjoy
```

## Step 4: Launch DeckJoy

From the Deck:

```bash
cd ~/Downloads/deckjoy
./deckjoy
```

Or add it to Steam as a Non-Steam Game:

```text
/home/deck/Downloads/deckjoy/deckjoy
```

The DeckJoy window has a **Start USB** button. Pressing that button is the critical step. Merely launching DeckJoy is not enough.

Before pressing **Start USB**, Windows did not see the Deck as a controller. After pressing it, Windows saw the USB composite HID device.

## Step 5: Avoid the Password Prompt Problem

In Gaming Mode, DeckJoy may ask for an admin password after **Start USB**, but the virtual keyboard may not appear. The clean fix is a narrow sudoers rule for the DeckJoy daemon.

Run this once in Konsole:

```bash
echo 'deck ALL=(ALL) NOPASSWD: /home/deck/Downloads/deckjoy/deckjoy daemon' | sudo tee /etc/sudoers.d/zzzdeckjoy
sudo chmod 440 /etc/sudoers.d/zzzdeckjoy
```

Test whether it works:

```bash
sudo -n /home/deck/Downloads/deckjoy/deckjoy daemon
```

If it starts without asking for a password, the sudoers rule is functional. Stop it with `Ctrl+C`.

Check the file:

```bash
sudo cat /etc/sudoers.d/zzzdeckjoy
sudo ls -l /etc/sudoers.d/zzzdeckjoy
```

Expected content:

```text
deck ALL=(ALL) NOPASSWD: /home/deck/Downloads/deckjoy/deckjoy daemon
```

Expected permission shape:

```text
-r--r----- 1 root root ... /etc/sudoers.d/zzzdeckjoy
```

Do not set an empty admin password. It is a bad security tradeoff, especially if SSH is enabled.

## Step 6: Verify on Windows

On Windows, first check Device Manager or use `pnputil`:

```powershell
pnputil /enum-devices /connected | Select-String -Pattern 'VID_1D6B|PID_0104|DeckJoy|game controller|HID'
```

The important entries are:

```text
USB\VID_1D6B&PID_0104
HID-compliant game controller
HID Keyboard Device
HID-compliant mouse
```

Then test the controller input:

```text
Win + R -> joy.cpl
```

Open the controller properties and press buttons or move sticks on the Deck.

Browser-based testers also work:

```text
https://hardwaretester.com/gamepad
https://gamepad-tester.com
```

## Debugging Checklist

If Windows does not see anything after plugging in USB-C:

1. Confirm USB DRD mode is enabled in firmware.
2. Confirm DeckJoy is running.
3. Confirm **Start USB** was actually pressed.
4. Check Deck-side gadget state:

```bash
ls /sys/class/udc
ls -l /dev/hidg*
find /sys/kernel/config/usb_gadget -maxdepth 4 -type f \
  \( -name idVendor -o -name idProduct -o -name product -o -name manufacturer -o -name UDC \) \
  -print -exec cat {} \;
```

When it works, `ls /sys/class/udc` should show something like:

```text
dwc3.1.auto
```

And `/dev/hidg*` should exist:

```text
/dev/hidg0
/dev/hidg1
/dev/hidg2
```

If DeckJoy is only running but USB was not started, there will be no gadget and no `/dev/hidg*` devices.

## Stopping DeckJoy

From the Deck:

```bash
pkill -TERM -f deckjoy
```

If a daemon remains owned by root, stop it from Konsole with sudo:

```bash
sudo pkill -TERM -f deckjoy
```

## Fixing the DeckJoy Window Size

In Desktop Mode, DeckJoy may render at the wrong scale. Launch it with an explicit Fyne scale:

```bash
cd ~/Downloads/deckjoy
FYNE_SCALE=1 ./deckjoy
```

If it is too large:

```bash
FYNE_SCALE=0.75 ./deckjoy
```

If it is too small:

```bash
FYNE_SCALE=1.25 ./deckjoy
```

For Steam launch options:

```text
FYNE_SCALE=1 %command%
```

## Why Some Buttons May Not Respond

DeckJoy reads the Deck's local joystick device from:

```text
/dev/input/js0
```

The USB joystick descriptor in DeckJoy supports 16 buttons. Some Steam Deck controls, especially rear grip buttons or Steam Input-only mappings, may not appear as normal `/dev/input/js0` joystick buttons.

If a button does not respond:

1. Open the Steam controller layout for DeckJoy.
2. Map that Deck button to a normal gamepad button such as `A`, `B`, `L3`, or `R3`.
3. Test again in `joy.cpl`.

If the button number is outside DeckJoy's supported range, DeckJoy would need a code change to expose more buttons.

## Final State

The final working system had:

- Steam Deck in USB DRD mode.
- DeckJoy installed at `/home/deck/Downloads/deckjoy`.
- A narrow sudoers rule for the DeckJoy daemon.
- DeckJoy running and **Start USB** activated.
- Windows detecting the Deck as a USB HID game controller, keyboard, and mouse.

The key lesson is that the USB cable alone does not make the Deck a controller. DeckJoy has to create the Linux USB gadget, and Windows only sees the controller after that gadget is active.
