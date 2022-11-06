# breakthecode
[Break The Code](https://boardgamearena.com/gamepanel?game=breakthecode) board game helper script

[![License: MPL](https://img.shields.io/github/license/zedaav/breakthecode)](https://github.com/zedaav/breakthecode/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/workflow/status/zedaav/breakthecode/Build/main?label=build%20%26%20u.t.)](https://github.com/zedaav/breakthecode/actions?query=branch%3Amain)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This script lists all the possible solutions to break the code, according to provided constraints.

## Install

Easy: **`pip install breakthecode`**

## Usage

```
usage: breakthecode [-h] [--remove DC] [--sum T[,I[,L[,C]]]] [--position N,I] [--odd O] [--even E] [--black B] [--white W] [--diff D] [--digit I<=>V] [--pairs P]

BreakTheCode board game helper

optional arguments:
  -h, --help            show this help message and exit
  --remove DC, -r DC    number that can't be part of the solution (e.g. 0b, 6w, 5)
  --sum T[,I[,L[,C]]], -s T[,I[,L[,C]]]
                        add a sum constraint (T=total, I=start, L=length, C=color)
  --position N,I, -p N,I
                        add a position constraint (N=number, I=position)
  --odd O, -o O         add an odd numbers count constraint
  --even E, -e E        add an even numbers count constraint
  --black B, -b B       add a black numbers count constraint
  --white W, -w W       add a white numbers count constraint
  --diff D, -d D        add a max-min diff constraint
  --digit I<=>V, -D I<=>V
                        add a digit comparison constraint (I=index, V=value)
  --pairs P, -P P       add a pairs count contraint
```
