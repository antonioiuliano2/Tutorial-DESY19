#!/bin/bash
#launched with deepcopy option in run_simScript.py
ProcId=$2
LSB_JOBINDEX=$((ProcId+1))
echo $LSB_JOBINDEX

SHIPBUILD_mymaster=/afs/cern.ch/work/a/aiuliano/public/SHIPBuild
export ALIBUILD_WORK_DIR=$SHIPBUILD_mymaster/sw #for alienv

echo "SETUP"
source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
eval `$ALIBUILD/alienv load FairShip/latest`

echo "start of simulation"

OUTPUTDIR=/afs/cern.ch/work/a/aiuliano/public/sim_desy19/RUN3_100runs_02_December_2020

which python

python $SHIPBUILD_mymaster/FairShip/macro/run_simScript.py --desy19 3 --PG --pID 11 -n 360 -o $OUTPUTDIR/$LSB_JOBINDEX

echo "end of simulation"
