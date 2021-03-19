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

DESYDIR=/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/Exercise_MariaChain

DESYMACROS=/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/macros

/cvmfs/ship.cern.ch/SHiP-2021/2020/November/16/sw/slc7_x86-64/Python/v3.6.8-1/bin/python3 $DESYMACROS/Dataset_preparation_ML_analysis/RUN3_simulazioni/Ricerca_new.py -n $LSB_JOBINDEX -is $DESYDIR/Inizio_sciame_RUN6.csv -it $DESYDIR/Theta/Dataset_tagli.csv -of $DESYDIR/Event
