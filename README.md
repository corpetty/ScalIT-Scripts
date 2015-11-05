# ScalIT-Scripts
A Python Scripting sytem to create input files and respective run scripts for running the **ScalIT** software suite.  

The system is built on creating Python classes as data structures to store parameters.  Once filled, you can perform
a variety of operations on them to facilitate using the ScalIT software suite.

## Methods for filling Python Classes

  - Fill in the relevant **ScalIT** variables in the mkO3.py file, which creates a large dictionary of dictionaries, and 
    then calls methods for creating class instances, which are then manipulated.  This is a primitive way of populating
    the class instances, but it was converted from old work.  Future methods will be more user-proof and easy to 
    understand.

## Platforms that have been implemented

  - local platform that runs **ScalIT**
  - Robinson HPCC at TTU
  - Hrothgar HPCC at TTU
  - Lonestar HPCC at UT Austin

## Systems that have been implemented

All triatomics that are currently implemented in **ScalIT**.  Future add-on methods will auto-load defaults for 
specific molecules.

## How to run

  1. Copy mkO3.py to another file, name it something relevant.  I tend to use the formality:
    - mk\<molecule name\>_\<mass option\>_<specific convergence test\>.py
  2. Input molecular variables, host, relevant directories, and convergence parameters to copied file.
    - The top of the file consists of typical parameters that are changed for each **ScalIT** run, and descriptions are
      above the variable name.
      - It should be noted that the following parameters are input as lists (in between square brackets), and all 
        permutations of these inputs correspond to a separate **ScalIT** run.
          - total angular momentum quantum number, J
          - Jacobi coordinate little r
          - Jacobi coordinate Big R
          - angular momentum quantum number associated with little r, j
    - The bottom section corresponds to advanced changes for **ScalIT** runs, mostly algorithmic changes.
  3. run python file to generate all input files and scripts to run them.