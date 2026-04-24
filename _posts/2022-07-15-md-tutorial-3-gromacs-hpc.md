---
title: 'Molecular Dynamics Tutorial — Part 3: Running GROMACS on HPC Clusters'
date: 2022-07-15
permalink: /posts/2022/07/md-tutorial-gromacs-hpc/
tags:
  - Molecular Dynamics
  - GROMACS
  - HPC
  - Tutorial
---

This is Part 3 of a short series on molecular dynamics. [Part 1](/posts/2022/07/md-tutorial-environment-setup/) covered shell access and Linux basics; [Part 2](/posts/2022/07/md-tutorial-software/) covered PyMOL, text editors, and the PDB format. Part 3 covers environment setup on HPC clusters (TACC and local), a brief primer on the physics behind MD, and a starting point for GROMACS simulations.

## Setting up the environment

### TACC

Check what software is available with `module avail`, then load GROMACS along with GCC:

```bash
module load gcc
module load gromacs
```

To avoid repeating this every session, append those `module load` lines to `~/.bashrc`:

```bash
vim ~/.bashrc
```

After saving, reload the shell configuration:

```bash
source ~/.bashrc
```

### Local cluster

Same idea, with MPICH and Slurm added:

```bash
module load gcc
module load mpich
module load slurm
module load gromacs
```

### Verifying the install

GROMACS is now available as `gmx` (TACC) or `gmx_mpi` (local cluster):

```bash
# TACC
gmx --version

# Local cluster
gmx_mpi --version
```

## Being a good TACC citizen

TACC users should skim the [Longhorn user guide](https://portal.tacc.utexas.edu/user-guides/longhorn) before launching anything real. The key points:

**Run I/O-heavy jobs (including `gmx`) from `$SCRATCH`, not `$HOME`:**

```bash
cd $SCRATCH
pwd
```

**Use `$WORK` for long-term file storage:**

```bash
cd $WORK
pwd
```

**Login nodes are for file management, not compute.** Any `gmx` command counts as a job — launch it via `idev` for an interactive session, or write a Slurm script and submit with `sbatch myscript.txt`:

```bash
idev -A CHE21040
```

## A short primer on molecular dynamics

At its core, MD solves Newton's equations of motion for individual particles (atoms and ions). Because the inter-particle distance is larger than the de-Broglie wavelength of typical molecules, the motion can be treated classically.

**Classical MD** (what we use here):

- Interactions are approximated by empirical pair potentials fit to experiment.
- Reduces to a purely classical many-particle problem.
- Works well for simple particles with isotropic interactions (e.g., noble gases).
- Works less well for covalent atoms (directional bonding) and metals (electron Fermi gas).
- Simulations are fast and permit large particle counts.

**Ab-initio MD** (not used here):

- Performs a full quantum calculation of electronic structure at every time step — "from first principles".
- Forces are derived from the energy dependence on atomic positions.
- Much higher accuracy, but much higher numerical cost — restricts particle count and simulation time.

### Physics background

For $N$ particles at positions $\vec{r}\_i$ $(i = 1, \ldots, N)$ with velocities $\dot{\vec{r}}\_i = \vec{p}\_i / m$:

**Kinetic energy:**

$$
E_\mathrm{kin} = \sum_{i=1}^{N} \frac{m_i}{2}\,\dot{\vec{r}}_i^{\,2}
= \sum_{i=1}^{N} \frac{\vec{p}_i^{\,2}}{2 m_i}
$$

**Potential energy** (inter-particle plus external):

$$
E_\mathrm{pot} = V_\mathrm{int}(\vec{r}_1, \ldots, \vec{r}_N)
+ \sum_{i=1}^{N} U_\mathrm{ext}^{(i)}(\vec{r}_i)
$$

**Forces:**

$$
\vec{F}_i = -\frac{\partial}{\partial \vec{r}_i}\, V_\mathrm{int}(\vec{r}_1, \ldots, \vec{r}_N)
- \frac{\partial}{\partial \vec{r}_i}\, U_\mathrm{ext}^{(i)}(\vec{r}_i)
$$

**Total energy:** $E = E\_\mathrm{kin} + E\_\mathrm{pot}$.

### The Lennard-Jones potential

A common choice for the interaction potential:

$$
V_\mathrm{int}(\vec{r}_1, \ldots, \vec{r}_N)
= \frac{1}{2} \sum_{\substack{i,j=1 \\ i \ne j}}^{N} V(\vec{r}_i - \vec{r}_j)
$$

with

$$
V(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]
$$

and a truncation distance $R\_c$:

$$
V_T(r) = \begin{cases}
V(r) - V(R_c) & r \le R_c \\
0             & r > R_c
\end{cases}
$$

### Time integration — the Verlet algorithm (1967)

The equations of motion are second-order ODEs for the positions $\vec{r}\_i$. They can be simplified because the forces depend only on $\vec{r}$, not on $\dot{\vec{r}}$:

$$
m_i\, \frac{d^2 \vec{r}_i}{dt^2} = \vec{F}_i(\vec{r}_1, \ldots, \vec{r}_N)
\qquad \Leftrightarrow \qquad
\frac{d^2 \vec{r}_i}{dt^2} = \vec{a}_i(\vec{r}_1, \ldots, \vec{r}_N)
$$

Verlet integration uses the central-difference approximation to the second derivative:

$$
\frac{d^2 \vec{r}_t}{dt^2}
= \frac{\vec{r}_{t+1} - 2\vec{r}_t + \vec{r}_{t-1}}{\Delta t^2}
= \vec{a}_t
$$

Taylor-expanding $\vec{r}(t \pm \Delta t)$ around $t = t\_n$:

$$
\begin{aligned}
\vec{r}_{t+\Delta t} &= \vec{r}_t + \vec{v}_t\,\Delta t + \frac{\vec{a}_t\,\Delta t^2}{2} + \frac{\vec{b}_t\,\Delta t^3}{6} + \mathcal{O}(\Delta t^4) \\
\vec{r}_{t-\Delta t} &= \vec{r}_t - \vec{v}_t\,\Delta t + \frac{\vec{a}_t\,\Delta t^2}{2} - \frac{\vec{b}_t\,\Delta t^3}{6} + \mathcal{O}(\Delta t^4)
\end{aligned}
$$

Adding the two gives the Verlet position update:

$$
\vec{r}_{t+\Delta t} = 2\vec{r}_t - \vec{r}_{t-\Delta t} + \vec{a}_t\,\Delta t^2 + \mathcal{O}(\Delta t^4)
$$

Subtracting and solving for velocity:

$$
\vec{v}_t = \frac{\vec{r}_{t+\Delta t} - \vec{r}_{t-\Delta t}}{2\,\Delta t} + \mathcal{O}(\Delta t^2)
$$

A typical **velocity-Verlet** step:

1. Half-step velocity:

    $$
    \vec{v}_{t + \tfrac{1}{2}\Delta t} = \vec{v}_t + \tfrac{1}{2}\,\vec{a}_t\,\Delta t
    $$

2. Full-step position:

    $$
    \vec{x}_{t + \Delta t} = \vec{x}_t + \vec{v}_{t + \tfrac{1}{2}\Delta t}\,\Delta t
    $$

3. Compute $\vec{a}\_{t + \Delta t}$ from the interaction potential (e.g., Lennard-Jones) using the updated position $\vec{x}\_{t + \Delta t}$ (Newton's 2nd law).

4. Full-step velocity:

    $$
    \vec{v}_{t + \Delta t} = \vec{v}_{t + \tfrac{1}{2}\Delta t} + \tfrac{1}{2}\,\vec{a}_{t + \Delta t}\,\Delta t
    $$

Periodic boundary conditions will be introduced in the next tutorial; the detailed algorithm is not covered here.

## Running GROMACS

With the environment set up, head over to the official [GROMACS tutorials](http://www.mdtutorials.com/gmx/) for the hands-on details.

Start with **[Tutorial 1: Lysozyme in Water](http://www.mdtutorials.com/gmx/lysozyme/index.html)**. Once the commands feel natural, jump straight to **[Tutorial 5: Protein–Ligand Complex](http://www.mdtutorials.com/gmx/complex/index.html)**.

A few notes from experience:

- I use the `charmm36_feb2021.ff` force field instead of the `charmm36_mar2019.ff` version referenced in the tutorial. Download the newer one when prompted.
- PyMOL can visualize trajectories if you convert the `.xtc` file to `.pdb` with `gmx trjconv`. Do not dump more than ~2000 frames per trajectory ($\#\mathrm{frames} = t / dt$) — PyMOL will crash for large systems. Never include water in the final exported trajectory.
- **Take detailed notes on every simulation you run.** Future-you will thank present-you the next time a reproducibility question comes up.

If anything breaks, find me. Enjoy.

## Further reading

- [TACC Longhorn user guide](https://portal.tacc.utexas.edu/user-guides/longhorn)
- [GROMACS 2020 manual](https://manual.gromacs.org/documentation/2020/)
- [CHARMM-GUI](https://charmm-gui.org/) — input generator for biomolecular simulations
- [CGenFF](https://cgenff.umaryland.edu/) — CHARMM General Force Field for small molecules
- [GROMACS command-line reference](https://manual.gromacs.org/documentation/2020/user-guide/cmdline.html)
