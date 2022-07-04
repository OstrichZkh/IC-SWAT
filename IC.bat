REM @ECHO OFF 
REM ********************************************************************* 
REM Calculate Index of Connectivity(IC) 
REM Sediment and Flow Connectivity By Borselli(2008) and Cavalli(2013) 
REM Slope:0.005-1m/m; Method: D-infinity(Tarboton,1997); Weight: CP-Factor of USLE-RUSLE
REM SoftWare Version: SAGA 4.0.1 
REM Language: Batch 
REM ********************************************************************** 
 
REM ********************************************************************** 
REM **********      ATTENTIONS: This is only used with Wathershed      ********* 
REM ********************************************************************** 
REM            Basic Data:DEM(Elevations),CP-Factor of USLE-RUSLE,LuccMask 
REM    LuccMask:give 0 value to road and urban areas and value 1 to other area  
REM ********************************************************************** 
REM Need Modified:Path to saga_cmd.exe;Path to working dir;WNAME;CellSize 
REM ********************************************************************** 
 
REM ****************************** PATHS ******************************** 
REM Path to saga_cmd.exe 
SET PATH=%PATH%;C:\Program Files (x86)\QGIS 3.12\apps\saga-ltr
 
REM Path to working dir 
SET WORK=C:\Users\yezouhua\Desktop\master\Paper2\DATA\IC
REM ********************************************************************** 
 
REM DEM:dem%WNAME%.dat, LuccMask:MASK%WNAME%.dat, Weight:ICW%WNAME%.dat
SET WNAME=s0
SET CELLSIZE=30

REM   ##############################     1 
REM Tool: Slope, Aspect, Curvature 
saga_cmd ta_morphometry 0 -ELEVATION=%WORK%\dem%WNAME%.dat  -SLOPE=%WORK%\a1Slope%WNAME%.sgrd  -ASPECT=%WORK%\a2Aspect%WNAME%.sgrd -C_GENE=NULL -C_PROF=NULL -C_PLAN=NULL -C_TANG=NULL -C_LONG=NULL -C_CROS=NULL  -C_MINI=NULL -C_MAXI=NULL -C_TOTA=NULL -C_ROTO=NULL -METHOD=6  -UNIT_SLOPE=2 -UNIT_ASPECT=0 
 
REM   ##############################     2 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\a1Slope%WNAME%.sgrd -XGRIDS=NULL  -RESULT=%WORK%\a3S%WNAME%.sgrd  -FORMULA=ifelse(g1^<0.5,0.005,ifelse(g1^>100,1,g1/100)) -NAME=Calculation  -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################     0-3 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\dem%WNAME%.dat  -XGRIDS=%WORK%\MASK%WNAME%.dat -RESAMPLING=0  -RESULT=%WORK%\a03LUCC%WNAME%.sgrd -FORMULA=ifelse(g1^>1,h1,h1)  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################      3 
REM Tool: Flow Accumulation (Top-Down) 
saga_cmd ta_hydrology 0 -ELEVATION=%WORK%\dem%WNAME%.dat  -SINKROUTE=NULL -WEIGHTS=%WORK%\a03LUCC%WNAME%.sgrd  -FLOW=%WORK%\a4AccMask%WNAME%.sgrd -VAL_INPUT=NULL  -ACCU_MATERIAL=NULL -STEP=1 -FLOW_UNIT=1 -FLOW_LENGTH=NULL  -LINEAR_DIR=NULL -METHOD=3 -LINEAR_DO=0 
 
REM   ##############################      5 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\a5RiverMask%WNAME%.sgrd  -XGRIDS=%WORK%\MASK%WNAME%.dat -RESAMPLING=0  -RESULT=%WORK%\a6MaskFinal%WNAME%.sgrd -FORMULA=g1*h1  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################      6 
REM Tool: Flow Accumulation (Top-Down) 
saga_cmd ta_hydrology 0 -ELEVATION=%WORK%\dem%WNAME%.dat  -SINKROUTE=NULL -WEIGHTS=%WORK%\a6MaskFinal%WNAME%.sgrd  -FLOW=%WORK%\a7AccF%WNAME%.sgrd -VAL_INPUT=NULL  -ACCU_MATERIAL=NULL -STEP=1 -FLOW_UNIT=1 -FLOW_LENGTH=NULL  -LINEAR_DIR=NULL -METHOD=3 -LINEAR_DO=0 -NO_NEGATIVES=1  -WEIGHT_LOSS=NULL 
 
REM   ##############################     7 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\a7AccF%WNAME%.sgrd -XGRIDS=NULL  -RESULT=%WORK%\a8AccFinal%WNAME%.sgrd -FORMULA=g1+1  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################     8 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\a3S%WNAME%.sgrd  -XGRIDS=%WORK%\ICW%WNAME%.dat -RESAMPLING=0  -RESULT=%WORK%\a9invCS%WNAME%.sgrd -FORMULA=1/g1/h1  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################     9 
REM Tool: Maximum Flow Path Length 
saga_cmd ta_hydrology 27 -ELEVATION=%WORK%\dem%WNAME%.dat  -WEIGHTS=%WORK%\a9invCS%WNAME%.sgrd  -DISTANCE=%WORK%\a10X%WNAME%.sgrd -DIRECTION=0 

REM   ##############################     10 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1  -GRIDS=%WORK%\a10X%WNAME%.sgrd;%WORK%\a9invCS%WNAME%.sgrd  -XGRIDS=NULL -RESULT=%WORK%\a11Ddn%WNAME%.sgrd  -FORMULA=ifelse(g1=0,g2,g1) -NAME=Calculation -FNAME=1 -USE_NODATA=0  -TYPE=7 
 
REM   ##############################     11 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1 -GRIDS=%WORK%\a6MaskFinal%WNAME%.sgrd  -XGRIDS=%WORK%\ICW%WNAME%.dat -RESAMPLING=0  -RESULT=%WORK%\a12CX%WNAME%.sgrd -FORMULA=g1*h1  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################     12 
REM Tool: Flow Accumulation (Top-Down) 
saga_cmd ta_hydrology 0 -ELEVATION=%WORK%\dem%WNAME%.dat  -SINKROUTE=NULL -WEIGHTS=%WORK%\a12CX%WNAME%.sgrd  -FLOW=%WORK%\a13AccCX%WNAME%.sgrd -VAL_INPUT=NULL  -ACCU_MATERIAL=NULL -STEP=1 -FLOW_UNIT=1 -FLOW_LENGTH=NULL  -LINEAR_DIR=NULL -METHOD=3 -LINEAR_DO=0 -NO_NEGATIVES=1  -WEIGHT_LOSS=NULL 
 
REM   ##############################     13 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1  -GRIDS=%WORK%\a6MaskFinal%WNAME%.sgrd;%WORK%\a3S%WNAME%.sgrd  -XGRIDS=NULL -RESULT=%WORK%\a14SX%WNAME%.sgrd -FORMULA=g1*g2  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
REM   ##############################     14 
REM Tool: Flow Accumulation (Top-Down) 
saga_cmd ta_hydrology 0 -ELEVATION=%WORK%\dem%WNAME%.dat  -SINKROUTE=NULL -WEIGHTS=a14SX%WNAME%.sgrd  -FLOW=%WORK%\a15AccSX%WNAME%.sgrd -VAL_INPUT=NULL  -ACCU_MATERIAL=NULL -STEP=1 -FLOW_UNIT=1 -FLOW_LENGTH=NULL  -LINEAR_DIR=NULL -METHOD=3 -LINEAR_DO=0 -NO_NEGATIVES=1  -WEIGHT_LOSS=NULL 
 
REM   ##############################     15 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1  -GRIDS=%WORK%\a13AccCX%WNAME%.sgrd;%WORK%\a8AccFinal%WNAME%.sgrd;%WORK%\a15AccSX%WNAME%.sgrd;%WORK%\a3S%WNAME%.sgrd  -XGRIDS=%WORK%\ICW%WNAME%.dat -RESAMPLING=0  -RESULT=%WORK%\a16Dup%WNAME%.sgrd  -FORMULA=(g1+h1)/g2*(g3+g4)/g2*sqrt(g2*%CELLSIZE%*%CELLSIZE%)  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7
 
REM   ##############################     16 
REM Tool: Grid Calculator 
saga_cmd grid_calculus 1  -GRIDS=%WORK%\a16Dup%WNAME%.sgrd;%WORK%\a11Ddn%WNAME%.sgrd  -XGRIDS=NULL -RESULT=a17IC%WNAME%.sgrd -FORMULA=log(g1/g2)  -NAME=Calculation -FNAME=1 -USE_NODATA=0 -TYPE=7 
 
PAUSE 
