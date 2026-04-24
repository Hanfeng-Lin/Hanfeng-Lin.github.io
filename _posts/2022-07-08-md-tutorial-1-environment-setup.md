---
title: 'Molecular Dynamics Tutorial — Part 1: Environment Setup and SSH Access'
date: 2022-07-08
permalink: /posts/2022/07/md-tutorial-environment-setup/
tags:
  - Molecular Dynamics
  - GROMACS
  - Linux
  - Tutorial
---

This is Part 1 of a short series on molecular dynamics. It covers the command-line environment you need on your laptop, how to SSH into our local Linux cluster or TACC, and a quick reference for the Linux commands you will live in. [Part 2](/posts/2022/07/md-tutorial-software/) covers PyMOL, text editors, and PDB structures; [Part 3](/posts/2022/07/md-tutorial-gromacs-hpc/) moves into GROMACS on HPC.

## Command-line environment

You need a Unix-style shell (BASH) to remote-control the Linux server. Windows `cmd` won't do — it is not a Unix shell. My recommendation for Windows is **Ubuntu on WSL**, but **PuTTY** also works.

### macOS

macOS is Unix-based, so `ssh` works out of the box from Terminal.app. Skip ahead to [Accessing the server](#accessing-the-server).

### Windows — Ubuntu on WSL

Ubuntu 20.04 LTS on Windows Subsystem for Linux gives you a minimal Linux environment.

**1. Update Windows.** Win10 or newer. Make sure the Anniversary Update is installed; WSL is unavailable without it.

**2. Enable Developer mode.**

- Open **Settings → Update & Security**
- Select the **For developers** tab in the left sidebar
- Turn on **Developer mode**

**3. Activate the Linux subsystem.**

- Open **Control Panel** (search, or scroll down the apps list → Windows System → Control Panel)
- Go to **Programs → Programs and Features**
- Click **Turn Windows features on or off** in the left sidebar
- Check **Windows Subsystem for Linux**
- Open the Microsoft Store, install **Ubuntu 20.04 LTS** ([aka.ms/wslstore](https://aka.ms/wslstore))
- Launch Ubuntu from the Start menu and create a Linux username + password when prompted
- Reboot

**4. Pick a BASH user mode.**

*Option 1 — normal user account (recommended).* Safer, but you'll type your password for `sudo` operations. Just launch Bash and create a username + password.

*Option 2 — root account.* You're always root, so no `sudo` is required. Open a Windows Command Prompt (not Bash) and run:

```bash
lxrun /install /y
```

**5. Install common tooling.** In a Bash window:

```bash
sudo apt-get update
sudo apt-get install ipython3 python3-setuptools python3-pip
```

Drop the `sudo` if you chose Option 2 above.

## Accessing the server

First, get an account. Contact Harmon for our local Linux cluster, or Jin for a TACC allocation.

### Local cluster

Our local server runs CentOS Linux 8. From Bash:

```bash
ssh yourusername@10.2.19.247
```

Enter your password when prompted. You should see something like:

```
Welcome to Bright release         9.1
                                        Based on CentOS Linux 8
                                                    ID: #821233

Use the following commands to adjust your environment:

'module avail'            - show available modules
'module add <module>'     - adds a module to your environment for this session
'module initadd <module>' - configure module to be loaded at every login
```

Your shell prompt now reads:

```
[username@wanglabs ~]$
```

The `~` means you're in your home directory. You are in.

### TACC

```bash
ssh username@longhorn.tacc.utexas.edu
```

You'll be asked for your password and a token code. To set up the token, sign in at the [TACC portal](https://portal.tacc.utexas.edu/) and follow the [Multi-Factor Authentication guide](https://portal.tacc.utexas.edu/account-profile).

### Exiting

```bash
[username@wanglabs ~]$ exit
logout
Connection to 10.2.19.247 closed.
```

## Appendix: Linux commands worth knowing

Look up the details individually as you need them — this is just a cheat sheet.

```bash
ssh                # connect to a remote server
cd                 # change directory
ls                 # list directory contents
ll                 # detailed listing (alias for `ls -l`)
mkdir              # make a new folder
chmod 754 <file>   # change permissions — look up 754 etc.
cp / scp           # copy; scp for between-server copies
mv                 # move / rename
rm                 # delete
tar -zxvf <file>   # extract a .tar.gz archive
vim <file>         # terminal text editor
less <file>        # quickly page through a file

sudo               # run as superuser (password required)
root               # full root permissions

sudo apt-get install <package>    # install a package (Ubuntu/Debian)

module avail                       # list available modules
module add <module>                # load a module this session
module initadd <module>            # load at every login

gmx                                # GROMACS on TACC
gmx_mpi                            # GROMACS on local cluster
```

Play with these until the common ones feel automatic.

### Finding WSL files from Windows

Your WSL home directory lives under:

```
C:\Users\<WinUser>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\rootfs\home\<Ubuntu_username>\
```

Useful when you need to drop a file into your Linux account without `scp`.

---

**Up next**: [Part 2 — Software: PyMOL, text editors, and PDB structure →](/posts/2022/07/md-tutorial-software/)

*Still to cover: Anaconda installation, PyMOL open-source 2.4 install, and a PDB format walkthrough — see Part 2.*
