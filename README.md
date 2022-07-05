# IC-SWAT
This is a demo, ic.bat file is used to calculate IC, IC-SWAT.py file is the core code of the model, some of which are incomplete. 
If necessary, you can contact me through email: 202021180019@mail.bnu.edu.cn

**The calibration process is as follows: **
(1) read the parameters related to soil phosphorus from SWAT files; 
(2) run SWAT model to obtain the spatial distribution of soil phosphorus every month; 
(3) calculate the on-site erosion with Eq.(1) and the SDR with Eq.(5); 
(4) estimate PP distribution with Eq.(7)-Eq.(9); 
(5) optimize the parameters on NSGA-III, and repeat the above steps until a satisfactory calibration result is obtained.
