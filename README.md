# An adaptive mechatronic exoskeleton for force-controlled finger rehabilitation
>This repository represents the source code for a novel mechatronic exoskeleton architecture for finger rehabilitation. The system consists of an underactuated kinematic structure that enables the exoskeleton to act as an adaptive finger stimulator. 


 <img src="results\all_in_one.png" alt="Drawing" style="width: 500px;">


## Setup

* Install Python (Recommended 3.6+)


## What does each file do? 

    .     
    ├── exoskeleton                      # Folder for solving the Exoskeleton Equations
    │   ├── exo_workflow.py              # contains the logic of the exoskeleton
    │   └── individual_params.py         # translate the pixel differences to parameter infos
    |
    ├── force_kalib                      # Folder for solving the force sensor calibration
    │   └── eval_forces.py               # calibrate
    |
    ├── poti_kalib                       # Folder for solving the potentiometer calibration
    │   └── poti_eval.py                 # calibrate
    |
    ├── results                          # Contains the final results
    |
    ├── videos                           # Contains the videos of the measurements
    |
    ├── utils.py                         # Utilities to load correct model and calibration
    ├── visualize.py                     # Contains long plot functions
    ├── rom.py                           # Range of Motion Analysis
    └── main.py                          # Main file to run for evaluation

# Citation

If you use this project in any of your work, please cite:

```
tbd.
```