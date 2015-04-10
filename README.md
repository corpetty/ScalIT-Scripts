# ScalIT-Scripts
A Python Scripting sytem to create input files and respective run scripts for running the ScalIT software suite.

## Platforms that have been implemented

  - local platform that runs **ScalIT**
  - Robinson HPCC at TTU
  - Hrothgar HPCC at TTU
  - Lonestar HPCC at UT Austin

## Systems that have been implemented

All triatomics that are currently implemented in ScalIT

## Convergence parameters that have been tested

Here is a table showing available options, all other parameters are held constant for each option:

|  Option | Convergence Parameter  |
|:-------:|:----------------------:|
|  -1     | run PRESINC            |
|  0      | jmax                   |
|  1      | theta                  |
|  2      | r                      |
|  3      | R                      |

## How to run

  1. Copy mkA3_template.py to a new file
  2. Input molecular variables, host, relevant directories, and convergence parameters
  3. run python file to generate all input files and scripts to run them.