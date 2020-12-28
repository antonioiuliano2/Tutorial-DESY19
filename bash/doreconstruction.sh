#!/bin/bash

#RUNFOLDER=7GeV
#cd $RUNFOLDER
#copying rootrc and making folders to store couples
cp $HOME/Lavoro/Tutorial-DESY19/FairShip2FEDRA/FairShip2Fedra.rootrc ./
mkdir b000003
mkdir b000003/p00{1..9}
mkdir b000003/p0{10..29}
#performing conversion
root -l $HOME/Lavoro/Tutorial-DESY19/FairShip2FEDRA/fromFairShip2Fedra.C

#going in reconstruction folder and copying required files for track reconstruction
cd b000003
cp $HOME/Lavoro/Tutorial-DESY19/FEDRA/scanset.sh ./
cp $HOME/Lavoro/Tutorial-DESY19/FEDRA/track.rootrc ./

source scanset.sh
emtra -set=3.0.0.0 -new -v=2
#preparing final csv

python $HOME/Lavoro/Tutorial-DESY19/scipy_conversion/csvconversion.py 3
