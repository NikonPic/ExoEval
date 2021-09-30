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
@ARTICLE{10.3389/frobt.2021.716451,
AUTHOR={Dickmann , Thomas and Wilhelm, Nikolas J. and Glowalla , Claudio and Haddadin , Sami and van der Smagt , Patrick and Burgkart , Rainer},    
TITLE={An Adaptive Mechatronic Exoskeleton for Force-Controlled Finger Rehabilitation},      
JOURNAL={Frontiers in Robotics and AI},      
VOLUME={8},      
PAGES={314},     
YEAR={2021},      
URL={https://www.frontiersin.org/article/10.3389/frobt.2021.716451},       
DOI={10.3389/frobt.2021.716451},      
ISSN={2296-9144},   
ABSTRACT={This paper presents a novel mechatronic exoskeleton architecture for finger rehabilitation. The system consists of an underactuated kinematic structure that enables the exoskeleton to act as an adaptive finger stimulator. The exoskeleton has sensors for motion detection and control. The proposed architecture offers three main advantages. First, the exoskeleton enables accurate quantification of subject-specific finger dynamics. The configuration of the exoskeleton can be fully reconstructed using measurements from three angular position sensors placed on the kinematic structure. In addition, the actuation force acting on the exoskeleton is recorded. Thus, the range of motion (ROM) and the force and torque trajectories of each finger joint can be determined. Second, the adaptive kinematic structure allows the patient to perform various functional tasks. The force control of the exoskeleton acts like a safeguard and limits the maximum possible joint torques during finger movement. Last, the system is compact, lightweight and does not require extensive peripherals. Due to its safety features, it is easy to use in the home. Applicability was tested in three healthy subjects.}
}
```