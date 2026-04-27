---
title: 'Diagnosing Photoshop 2026 Auto-Crash on Windows 11: A Deep Dive'
date: 2026-04-25
permalink: /posts/2026/04/photoshop-2026-bex64-nvidia-driver/
tags:
  - Windows
  - Photoshop
  - Debugging
  - NVIDIA
  - GPU Driver
  - WER
---

> Adobe Photoshop 2026 was crashing every 60–100 seconds on a Windows 11 box with a Quadro P5000. Every crash had the same `BEX64` signature at the same fault offset — a tell-tale sign of deterministic external interference, not random memory corruption. After ~2 hours of systematic elimination through hook DLLs, compatibility shims, preferences, and feature flags, the culprit turned out to be a 20-month-old NVIDIA enterprise driver. This post is the full diagnostic trail.

**Environment**

| | |
|---|---|
| **Platform** | Windows 11 Pro 24H2 (Build 26100) |
| **Application** | Adobe Photoshop 2026 v27.5.0.13 |
| **GPU** | NVIDIA Quadro P5000 |
| **Resolution Time** | ~2 hours of systematic elimination |

## The Symptom

Photoshop crashed automatically every few minutes without any user interaction. The crash was entirely reproducible — Photoshop would launch normally, appear fully functional, then terminate between 60–100 seconds after startup with no warning.

## Step 1: Reading the Windows Event Log

The first move was checking the Windows Application Event Log for crash signatures.

**Finding:** Two distinct events logged every crash session:

- **Event ID 1001 / `RADAR_PRE_LEAK_64`** — Windows detected a memory leak in Photoshop before the crash.
- **Event ID 1000 / `BEX64`** — A 64-bit Buffer Overflow Exception, crashing in `ntdll.dll` at offset `0x0000000000121650` with exception code `0xc0000409` (`STATUS_STACK_BUFFER_OVERRUN`).

```
Faulting application: Photoshop.exe v27.5.0.13
Faulting module:      ntdll.dll
Exception code:       0xc0000409  (STATUS_STACK_BUFFER_OVERRUN)
Exception data:       0x000000000000000a  (FAST_FAIL_STACK_COOKIE_CHECK_FAILURE)
Fault offset:         0x0000000000121650
```

The identical fault offset across every crash told us this was **deterministic** — the same code path failing every time, not random memory corruption.

**Initial hypothesis:** Memory exhaustion triggering a latent bug. System RAM was nearly full (only 1.4 GB free of 32 GB) due to Chrome, multiple VS Code instances, and other heavy processes.

## Step 2: Eliminating Memory as the Primary Cause

After freeing RAM, Photoshop continued to crash with the exact same signature. Memory pressure contributed to earlier RADAR events but was not the root cause.

## Step 3: Analyzing the WER Crash Report

Windows Error Reporting archives a `Report.wer` file for each crash, containing the full list of DLLs loaded into the process at crash time. Scanning the `LoadedModule[]` entries for non-Adobe, non-Windows DLLs revealed two injected hook DLLs:

```
LoadedModule[157] = C:\Program Files\Listary\ListaryHook64.dll
LoadedModule[195] = C:\Program Files\NVIDIA Corporation\nview\nViewH64.dll
```

Both **Listary** (a file search utility) and **NVIDIA RTX Desktop Manager** inject hook DLLs into running applications. Hook DLLs are a classic cause of `BEX64` crashes because they modify stack behavior inside the target process.

**Action:** Quit Listary, then uninstall NVIDIA RTX Desktop Manager.

**Result:** Crash continued. However, both DLLs disappeared from subsequent crash reports, confirming they were eliminated — but they were not the root cause.

## Step 4: Discovering a Windows Compatibility Shim

With hook DLLs gone, three Windows compatibility DLLs persisted in every crash report:

```
LoadedModule[4]  = C:\WINDOWS\SYSTEM32\apphelp.dll
LoadedModule[5]  = C:\WINDOWS\SYSTEM32\AcGenral.dll
LoadedModule[26] = C:\WINDOWS\SYSTEM32\AcLayers.DLL
```

`AcLayers.DLL` is only loaded when a **Windows compatibility layer** is active. Checking the registry confirmed the culprit:

```
HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers
"C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe" = "~ WIN8RTM"
```

Photoshop had been set to run in **Windows 8 RTM compatibility mode** at some point — likely by accident via the Properties → Compatibility tab. This caused Windows to inject `AcLayers.DLL` into every Photoshop process, which hooked `ntdll.dll` in a way that was incompatible with PS 2026's stack layout.

**Action:** Removed the registry entry.

```powershell
Remove-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" `
    -Name "C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe"
```

**Result:** `AcLayers.DLL` disappeared from crash reports. `AcGenral.dll` remained (loaded by Windows' built-in system compatibility database, unrelated to the user-set flag). Crash continued.

## Step 5: Eliminating Corrupted Preferences and Cache

With all known external factors removed, the next hypothesis was corrupted local data. Three locations were backed up and cleared:

| Location | Purpose |
|---|---|
| `AppData\Roaming\Adobe\CCX Welcome\` | Home screen content cache |
| `AppData\Roaming\Adobe\UXP\PluginsStorage\PHSP\27\` | UXP plugin storage |
| `AppData\Roaming\Adobe\Adobe Photoshop 2026\Adobe Photoshop 2026 Settings\` | All Photoshop preferences |

The UXP logs had consistently shown this error during startup:

```
[Error] [FallbackComponent] Failed to render layout for home route!
         Error: Home Yukon data is corrupt or not present: undefined
```

**Result:** Crash continued with fresh preferences. Corrupted data was ruled out.

## Step 6: Systematic Feature Isolation

Since no external cause remained, each internal subsystem was disabled in turn:

| Test | Method | Result |
|---|---|---|
| Disable GPU acceleration | `PSUserConfig.txt` with `UseGPU 0` | No effect — PS 2026 ignores this file |
| Run as Administrator | `Start-Process -Verb RunAs` | Crashed at ~100s |
| Windows 7 compat mode | Registry `~ WIN7RTM` | Crashed at ~100s |
| Launch with file argument | `Photoshop.exe test.bmp` (bypasses home screen) | Crashed at ~80s |
| Disable Camera Raw plugin | Renamed `Camera Raw.8bi` | Crashed faster (~20s) |

None of these changed the outcome. The crash was happening in Photoshop's native C++ code during background initialization, independent of user configuration.

## Step 7: Pinpointing the GPU Driver

The UXP log showed Photoshop's home screen fully loading at T+35s, with the crash following 40+ seconds later. Analysis of what loads and initializes in that window pointed to the GPU pipeline — specifically **DirectX 12 and OpenCL compute initialization**, which Photoshop 2026 performs asynchronously after the UI is ready.

The loaded modules in every crash dump included the NVIDIA Quadro P5000 user-mode driver:

```
nvwgf2umx.dll   (NVIDIA D3D12 user-mode driver)
nvgpucomp64.dll (NVIDIA GPU compute)
nvopencl64.dll  (NVIDIA OpenCL)
```

The installed driver was **v560.94, dated August 14, 2024** — 20 months old at the time of the crash.

**Definitive test:** Disable the NVIDIA Quadro P5000 entirely via Device Manager, then launch Photoshop.

```powershell
Disable-PnpDevice -InstanceId "PCI\VEN_10DE&DEV_1BB0&SUBSYS_11B210DE&REV_A1\4&386B0AD6&0&0008" -Confirm:$false
```

**Result:** Photoshop ran for 3+ minutes without crashing. With the GPU re-enabled and the old driver, it crashed within 60–100 seconds every time. **The NVIDIA driver was the confirmed root cause.**

## Root Cause

The NVIDIA Quadro P5000 driver v560.94 contained a **stack buffer overflow** in its DirectX 12 / GPU compute initialization path. When Photoshop 2026 called into the driver to initialize its AI/GPU pipeline (ONNX Runtime, DirectML, D3D12 command queues), the driver overflowed a stack buffer. Windows' stack cookie protection (`__security_check_cookie`) caught the corruption and terminated the process via `ntdll!RtlFailFast` — always at the same address, always with the same exception.

The overflow was deterministic because Photoshop 2026 always makes the same GPU API calls in the same order during startup.

## Fix

Update the NVIDIA Quadro P5000 driver from the NVIDIA enterprise driver portal:

> nvidia.com → Drivers → Product Type: NVIDIA RTX/Quadro → P-Series → Quadro P5000

Updated to **v582.41 (March 5, 2026)**. After the update:

```
20s:  Running
40s:  Running
...
180s: Running
Survived 3 minutes — FIXED!
```

## Lessons Learned

**1. Read the WER crash report's `LoadedModule` list.** Third-party hook DLLs are invisible in normal troubleshooting but appear clearly here. Two injected DLLs (Listary, nView) were found and eliminated this way.

**2. Deterministic crashes (`BEX64`, same fault offset every time) are external interference or driver bugs — not random memory issues.** Random heap corruption produces different offsets on each crash.

**3. `PSUserConfig.txt` is not supported in Photoshop 2026.** The commonly cited `UseGPU 0` trick no longer works; disabling GPU requires Device Manager or the Preferences UI.

**4. Enterprise GPU drivers fall behind consumer drivers.** NVIDIA Quadro / RTX Enterprise drivers are not auto-updated by Windows Update or GeForce Experience. They must be downloaded manually from NVIDIA's enterprise portal, and falling 12–24 months behind is easy to miss.

**5. Systematic elimination beats guesswork.** The actual root cause (GPU driver) was the last thing tested — but each eliminated step built confidence and narrowed the search space rather than wasting time on reinstalls or OS repairs.

## Troubleshooting Checklist for Photoshop BEX64 Crashes

- [ ] Check Event Viewer → Application log for Event ID 1000/1001 on `Photoshop.exe`
- [ ] Open `Report.wer` in the WER archive, scan `LoadedModule[]` for non-Adobe/non-Windows DLLs
- [ ] Check `HKCU\...\AppCompatFlags\Layers` for any compatibility mode on `Photoshop.exe`
- [ ] Clear `CCX Welcome` cache and UXP plugin storage
- [ ] Reset Photoshop preferences folder
- [ ] Disable NVIDIA GPU in Device Manager and test — if fixed, update the driver from NVIDIA enterprise portal
- [ ] If crash persists without GPU: update Photoshop via Creative Cloud
