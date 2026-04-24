---
title: 'Molecular Dynamics Tutorial — Part 2: PyMOL, Text Editors, and PDB Structure'
date: 2022-07-15
permalink: /posts/2022/07/md-tutorial-software/
tags:
  - Molecular Dynamics
  - PyMOL
  - PDB
  - Tutorial
---

This is Part 2 of a short series on molecular dynamics. [Part 1](/posts/2022/07/md-tutorial-environment-setup/) covered shell access and Linux basics; Part 2 covers the desktop software you'll want before diving into simulations, and a quick tour of the PDB file format. [Part 3](/posts/2022/07/md-tutorial-gromacs-hpc/) moves into GROMACS on HPC.

## Visualization software

### PyMOL

First install [Anaconda](https://www.anaconda.com/), then pull down **PyMOL open-source v2.4** through conda-forge. Open the Anaconda Prompt (Windows Start menu → run as administrator) and run:

```bash
conda install -c conda-forge pymol-open-source
```

Launch it afterwards with `pymol` at the prompt.

### VMD (alternative)

[VMD](https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD) is an alternative for visualization and trajectory analysis. Either works — pick the one whose interface you get along with.

## Text editors

### VSCode

I use **[VSCode](https://code.visualstudio.com/download)** as my main editor. Two reasons it pays off for MD work:

- Plugins render `.pdb` and parameter files with syntax highlighting
- **Column editing** (`Alt`-drag or `Ctrl+Shift+Alt+Arrow`) is indispensable when hand-editing parameter files

### Vim

On the server side, **vim** is your default. Launch it with:

```bash
vim file.txt
```

If `vim` isn't installed:

```bash
sudo apt-get install vim
```

Vim has several modes, but in practice you live in **command mode** and **insert mode**.

**Command mode** is the default on startup (or press `Esc` to return). Use it to navigate the file and run last-line commands (those beginning with `:`), for example:

- `:w` — save
- `:q` — quit
- `:wq` — save and quit
- `:q!` — force quit without saving

**Insert mode** lets you type text into the file. Enter it by pressing `i`. Remember to press `Esc` before `:w` — commands only work in command mode.

A handy cheat sheet:

![Vim cheat sheet](https://1808197252-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-LVVKHMnpflHwghmbdgi%2F-LqnJzGmUntizDaSIDeF%2F-LqnK441fKXw2ZWfSfLo%2Fvi-vim-cheat-sheet.gif?alt=media&token=631c3045-6d64-4cce-8650-114c73e16ed8)

## PDB file structure

The Protein Data Bank (PDB) format is fixed-column; every field sits at a specific character position.

![PDB format column layout](https://rna-tools.readthedocs.io/en/latest/_images/pdb_format_numbering.png)

The field you'll most often change by hand is the **chain identifier** (column 22, field 6 in the diagram).

Two other records to know:

- **`HETATM`** records appear at the end of the file when the structure contains ligands or other non-standard residues.
- **`CONECT`** records describe explicit bonds between specified atoms — essential when ligand chemistry needs to survive the force-field assignment.

## Repairing missing loops

Experimentally determined structures routinely have missing residues or loops that weren't resolved in the electron density. Fix them before simulation — otherwise your MD starts from a structurally broken input.

I use **[Modeller 10.3](https://salilab.org/modeller/release.html)** for this. The missing-residue workflow is documented in the [Modeller wiki](https://salilab.org/modeller/wiki/Missing%20residues), and you'll write a short Python driver script to point Modeller at your structure.

The process is fiddly and laborious the first time. Read the wiki page carefully, and find me if you're stuck.

---

**Up next**: [Part 3 — Running GROMACS on HPC clusters →](/posts/2022/07/md-tutorial-gromacs-hpc/)
