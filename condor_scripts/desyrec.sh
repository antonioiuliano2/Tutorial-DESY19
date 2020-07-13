#!/bin/bash
#launched with deepcopy option in run_simScript.py
ProcId=$2
LSB_JOBINDEX=$((ProcId+1))
echo $LSB_JOBINDEX

SHIPBUILD_mymaster=/afs/cern.ch/work/a/aiuliano/public/SHIPBuild
export ALIBUILD_WORK_DIR=$SHIPBUILD_mymaster/sw #for alienv

echo "SETUP"
source /cvmfs/ship.cern.ch/SHiP-2020/latest/setUp.sh
eval `alienv load FairShip/latest`
source /afs/cern.ch/work/a/aiuliano/public/fedra/setup_new.sh

echo "start of conversion"

OUTPUTDIR=/afs/cern.ch/work/a/aiuliano/public/sim_desy19/RUN3_100runs_movingtarget_12_july_2020

mkdir $OUTPUTDIR/$LSB_JOBINDEX/b000003
mkdir $OUTPUTDIR/$LSB_JOBINDEX/b000003/p00{1..9}
mkdir $OUTPUTDIR/$LSB_JOBINDEX/b000003/p0{10..29}

cp $OUTPUTDIR/FairShip2Fedra.rootrc $OUTPUTDIR/$LSB_JOBINDEX/
cp $OUTPUTDIR/track.rootrc $OUTPUTDIR/$LSB_JOBINDEX/b000003
cp $OUTPUTDIR/scanset.sh $OUTPUTDIR/$LSB_JOBINDEX/b000003

cd $OUTPUTDIR/$LSB_JOBINDEX/

root -l $OUTPUTDIR/fromFairShip2Fedra.C

echo "end of conversion, starting reconstruction"

cd $OUTPUTDIR/$LSB_JOBINDEX/b000003

source scanset.sh

emtra -set=3.0.0.0 -new -v=2

python /eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/macros/scipy_conversion/csvconversion.py 3
