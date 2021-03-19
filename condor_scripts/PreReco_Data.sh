#!/bin/bash
#launched with deepcopy option in run_simScript.py
ProcId=$2
LSB_JOBINDEX=$((ProcId+0))
echo $LSB_JOBINDEX

sleep $ProcId

SHIPBUILD_mymaster=/afs/cern.ch/work/a/aiuliano/public/SHIPBuild
export ALIBUILD_WORK_DIR=$SHIPBUILD_mymaster/sw #for alienv

echo "SETUP"
source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
eval `alienv load FairShip/latest`

DESYDIR=/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/RUN5_dataML

DESYMACROS=/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/macros

echo "Starting Rect code"
/cvmfs/ship.cern.ch/SHiP-2021/2020/November/16/sw/slc7_x86-64/Python/v3.6.8-1/bin/python3 $DESYMACROS/Dataset_preparation_ML_analysis/RUN3_Dati/Data_rect.py -n $LSB_JOBINDEX -is $DESYDIR/Inizio_candidati_sciami.csv -ir $DESYDIR/RUN5data_ric.csv -of $DESYDIR/Rect

echo "Starting Rect_crescenti code"
/cvmfs/ship.cern.ch/SHiP-2021/2020/November/16/sw/slc7_x86-64/Python/v3.6.8-1/bin/python3 $DESYMACROS/Dataset_preparation_ML_analysis/RUN3_Dati/Data_rect_crescenti.py -n $LSB_JOBINDEX -is $DESYDIR/Inizio_candidati_sciami.csv -if $DESYDIR/Rect -of $DESYDIR/Rect_crescenti

echo "Starting Theta code"
/cvmfs/ship.cern.ch/SHiP-2021/2020/November/16/sw/slc7_x86-64/Python/v3.6.8-1/bin/python3 $DESYMACROS/Dataset_preparation_ML_analysis/RUN3_Dati/Data_taglio_Theta.py -n $LSB_JOBINDEX -is $DESYDIR/Inizio_candidati_sciami.csv -if $DESYDIR/Rect_crescenti -of $DESYDIR/Theta

