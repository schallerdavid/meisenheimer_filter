# Meisenheimer Filter
Filter molecules for substructures able to form a Meisenheimer complex.

## Install

#### Clone this repository

Open a new terminal and clone this repository
```bash
cd ~
git clone https://github.com/schallerdavid/meisenheimer_filter
```

#### Install dependencies

Meisenheimer Filter is written in Python 3 and uses RDKit wich can be easily installed using conda:

```bash
conda create -n meisenheimer_filter -c conda-forge rdkit python=3.8
```

#### Create alias for your bash

```bash
echo 'alias meisenheimer_filter="python3 ~/meisenheimer_filter/meisenheimer_filter.py"' >> ~/.bashrc
```

## Use example

#### Load conda environment

Activate conda environment.
```bash
source activate meisenheimer_filter
```

Filter molecules for substructures.
```bash
meisenheimer_filter -i input.sdf -o output.sdf
```

## Copyright

Copyright (c) 2020, David Schaller
