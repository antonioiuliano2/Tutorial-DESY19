#!/bin/bash
#launched with deepcopy option in run_simScript.py
ProcId=$2
LSB_JOBINDEX=$((ProcId+1))
echo $LSB_JOBINDEX

OUTPUTDIR=/afs/cern.ch/work/a/aiuliano/public/sim_desy19/RUN3_100runs_02_December_2020/
FILE=$OUTPUTDIR/$LSB_JOBINDEX/b000003/p001/3.1.0.0.cp.root

if [[ -f "$FILE" ]]; then
    echo "$FILE already exists."
    exit 1
fi

SHIPBUILD_mymaster=/afs/cern.ch/work/a/aiuliano/public/SHIPBuild
export ALIBUILD_WORK_DIR=$SHIPBUILD_mymaster/sw #for alienv

echo "SETUP"
source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
eval `$ALIBUILD/alienv load FairShip/latest`
source /afs/cern.ch/work/a/aiuliano/public/fedra/setup_new.sh

echo "start of conversion"


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

export PYTHONPATH=$PYTHONPATH:/eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/macros/scipy_conversion/
python /eos/user/a/aiuliano/public/sims_FairShip/sim_DESY19/macros/scipy_conversion/csvconversion.py 3
