#!/bin/bash
#performing all reconstruction, FairShip2Fedra.rootrc and showerrec.rootrc need to be set in folder
NRUN=7 
#RUNFOLDER=7GeV
#cd $RUNFOLDER
#copying rootrc and making folders to store couples
mkdir b00000$NRUN
mkdir b00000$NRUN/p00{1..9}
mkdir b00000$NRUN/p0{10..29}

cp showerrec.rootrc b00000$NRUN/
#performing conversion
root -l -q $DESYMACROS/FairShip2FEDRA/fromFairShip2Fedra.C

#going in reconstruction folder and copying required files for track reconstruction
cd b00000$NRUN
echo "makescanset -set="$NRUN".0.0.0 -suff=cp.root -dz=-1315 -from_plate=29 -to_plate=1">scanset.sh
cp $DESYMACROS/FEDRA/track.rootrc ./

source scanset.sh
emtra -set=$NRUN.0.0.0 -new -v=2
#preparing final csv

python $DESYMACROS/scipy_conversion/csvconversion.py $NRUN

ln -s b00000$NRUN.0.0.0.trk.root linked_tracks.root
root -l -q $DESYMACROS/shower_reconstruction/shower_reconstruction.C
