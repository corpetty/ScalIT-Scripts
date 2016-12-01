# ScalIT-Scripts

**NOTE: THIS INFORMATION IS DEPRECATED, AND NEEDS UPDATING**

A Python Scripting sytem to create input files and respective run scripts for running the **ScalIT** software suite.  

The system is built on creating Python classes as data structures to store parameters.  Once filled, you can perform
a variety of operations on them to facilitate using the ScalIT software suite.

## Methods for filling Python Classes

  - Fill in the relevant **ScalIT** variables in molecular parameters file.  Running ScriptIT.py with this file as an argument
    creates a large dictionary of dictionaries, and then calls methods for creating class instances, based on which option you 
    choose from the main menu.

## Platforms that have been implemented

  - local platform that runs **ScalIT**
  - Robinson HPCC at TTU
  - Hrothgar HPCC at TTU
  - Lonestar5 HPCC at UT Austin
  - Eter HPCC at Initituto Tecnologico de Aeronautica, SP, Brasil

## Molecular systems that have been implemented

All triatomics and tetraatomics that are currently implemented in **ScalIT** can be generated.
  The only molecular default parameter files that exist are
  
  - triatomic molecules:
    - HO_2
  - tetraatomic molecules:
    - Ne_4

## Requirements
  1. Python 3.2 or greater
  2. itertools package
  3. posixpath package
  4. shlex package

## How to run

1. Copy a default molecular parameter file from the "Molecular Defaults" directory
    - give it a specific name based on your main parameters, I use:
        - \<molecule name\>_\<mass_label\>_\<permutation\>\<parity\>.py
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
3. run the ScriptIT.py file with your parameter file as an argument.
    - For example:
  ```
  $> python ScriptIT.py O3_o16o16o16_eveneven.py 
  ```
    
